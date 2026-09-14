"""Проверка пользовательских решений.

Каждое решение выполняется в отдельном процессе (subprocess, свой интерпретатор
sys.executable). Пользовательский код вставляется в runner-скрипт вместе с
тест-кейсами; результаты runner пишет в json-файл, который читает сервер.

Вердикты:
    accepted      — все выбранные тесты прошли;
    wrong_answer  — хотя бы один тест не прошёл;
    runtime_error — исключение в пользовательском коде;
    timeout       — превышен лимит времени (timeout_ms + запас);
    syntax_error  — синтаксическая ошибка в коде пользователя;
    no_tests      — у задачи нет тест-кейсов (только «ручная» проверка).

Конвертеры аргументов/результата (arg_converters / result_converter) — имена
функций в коде пользователя (например "_build"/"_to_list" для связных списков,
"attr:val" для доступа к атрибуту результата). case.sort_result — сравнивать
вложенные списки независимо от порядка.
"""
import json
import subprocess
import sys

from src import config
from src.core.registry import Problem, TestCase

# Стартовый запас на запуск интерпретатора (сек), поверх timeout_ms задачи.
_STARTUP_SLACK_SEC = 5.0
_MIN_TIMEOUT_SEC = 2.0


def _json_safe(value):
    """Рекурсивно привести значение к JSON-представимому виду (для ответа API)."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if value != value or abs(value) == float("inf"):  # NaN / ±inf
            return None
        return value
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    return str(value)


def _build_runner(problem: Problem, code: str, cases: list[TestCase]) -> str:
    """Собрать runner-скрипт: пользовательский код + вызов entry_function на кейсах.

    Конкатенация вместо .format() — безопасна относительно {} в JSON/пользовательском коде.
    """
    payload = [
        {
            "id": c.id,
            "args": c.args,
            "expected": c.expected,
            "arg_converters": c.arg_converters,
            "result_converter": c.result_converter,
            "sort_result": c.sort_result,
        }
        for c in cases
    ]
    cases_json = json.dumps(payload, ensure_ascii=False)
    entry = problem.entry_function or "_no_entry"
    return (
        "# -*- coding: utf-8 -*-\n"
        "import json as _json\n"
        "import sys as _sys\n"
        "\n"
        "_CASES = _json.loads(" + repr(cases_json) + ")\n"
        "_ENTRY = " + repr(entry) + "\n"
        "\n"
        "\n"
        "def _eq(a, b):\n"
        "    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):\n"
        "        return len(a) == len(b) and all(_eq(x, y) for x, y in zip(a, b))\n"
        "    return a is b or a == b\n"
        "\n"
        "\n"
        "def _sort2d(x):\n"
        "    if isinstance(x, (list, tuple)):\n"
        "        return sorted(\n"
        "            [sorted(g) if isinstance(g, (list, tuple)) else g for g in x],\n"
        "            key=repr,\n"
        "        )\n"
        "    return x\n"
        "\n"
        "\n"
        "def _convert_arg(value, name):\n"
        "    if not name:\n"
        "        return value\n"
        "    fn = globals().get(name)\n"
        '    if fn is None:\n'
        '        raise NameError("convert arg not found: " + name)\n'
        "    return fn(value)\n"
        "\n"
        "\n"
        "def _convert_result(got, spec):\n"
        "    if not spec:\n"
        "        return got\n"
        '    if isinstance(spec, str) and spec.startswith("attr:"):\n'
        '        return getattr(got, spec[5:], None)\n'
        "    fn = globals().get(spec)\n"
        '    if fn is None:\n'
        '        raise NameError("convert result not found: " + spec)\n'
        "    return fn(got)\n"
        "\n"
        "\n"
        "def _safe(value):\n"
        "    if value is None or isinstance(value, (bool, int, str)):\n"
        "        return value\n"
        "    if isinstance(value, float):\n"
        '        return value if value == value and abs(value) != float("inf") else None\n'
        "    if isinstance(value, (list, tuple)):\n"
        "        return [_safe(v) for v in value]\n"
        "    if isinstance(value, dict):\n"
        "        return {str(k): _safe(v) for k, v in value.items()}\n"
        "    return str(value)\n"
        "\n"
        "# <<USER_CODE>>\n"
        + code
        + "\n# <</USER_CODE>>\n"
        "\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    import time as _time\n"
        "\n"
        "    results = []\n"
        "    started = _time.perf_counter()\n"
        "    for case in _CASES:\n"
        "        try:\n"
        "            args = []\n"
        '            converters = case.get("arg_converters") or []\n'
        '            for i, raw in enumerate(case["args"]):\n'
        "                con = converters[i] if i < len(converters) else None\n"
        "                args.append(_convert_arg(_json.loads(_json.dumps(raw)), con))\n"
        "            fn = globals().get(_ENTRY)\n"
        '            if fn is None:\n'
        '                raise NameError("entry function not found: " + str(_ENTRY))\n'
        '            got = _convert_result(fn(*args), case.get("result_converter"))\n'
        '            expected = case["expected"]\n'
        '            if case.get("sort_result"):\n'
        "                got = _sort2d(got)\n"
        "                expected = _sort2d(expected)\n"
        "            results.append({\n"
        '                "id": case["id"],\n'
        "                \"passed\": bool(_eq(got, expected)),\n"
        '                "expected": _safe(expected),\n'
        '                "actual": _safe(got),\n'
        '                "error": None,\n'
        "            })\n"
        "        except Exception as exc:\n"
        "            results.append({\n"
        '                "id": case["id"],\n'
        '                "passed": False,\n'
        '                "expected": _safe(case.get("expected")),\n'
        '                "actual": None,\n'
        '                "error": type(exc).__name__ + ": " + str(exc),\n'
        "            })\n"
        "    elapsed = round((_time.perf_counter() - started) * 1000, 1)\n"
        '    with open(_sys.argv[1], "w", encoding="utf-8") as fh:\n'
        '        _json.dump({"results": results, "time_ms": elapsed}, fh, ensure_ascii=False)\n'
    )


def _extract_error(stderr: str) -> str:
    """Последняя строка traceback (тип + сообщение)."""
    lines = [line.strip() for line in stderr.splitlines() if line.strip()]
    return lines[-1] if lines else "execution failed"


def run_checks(problem: Problem, code: str, hide_hidden: bool = True) -> dict:
    """Запустить код пользователя на тест-кейсах задачи.

    hide_hidden=True  — только открытые (примеры) кейсы: эндпоинт /run.
    hide_hidden=False — все кейсы, включая скрытые: эндпоинт /submit.
    """
    cases = [c for c in problem.test_cases if not c.hidden] if hide_hidden else problem.test_cases
    if not cases:
        return {"verdict": "no_tests", "results": [], "time_ms": 0, "error": None}

    runner = _build_runner(problem, code, cases)
    timeout_sec = max(_MIN_TIMEOUT_SEC, problem.timeout_ms / 1000) + _STARTUP_SLACK_SEC
    config.SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = config.SOLUTIONS_DIR / f"_{problem.id}_run.json"

    try:
        proc = subprocess.run(
            [sys.executable, "-c", runner, str(out_path)],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(config.DATA_DIR),
        )
    except subprocess.TimeoutExpired:
        return {
            "verdict": "timeout",
            "results": [],
            "time_ms": int(timeout_sec * 1000),
            "error": f"Превышен лимит времени ({problem.timeout_ms} мс)",
        }

    if proc.returncode != 0:
        stderr = proc.stderr
        if "SyntaxError" in stderr:
            return {
                "verdict": "syntax_error",
                "results": [],
                "time_ms": 0,
                "error": _extract_error(stderr),
            }
        return {
            "verdict": "runtime_error",
            "results": [],
            "time_ms": 0,
            "error": _extract_error(stderr),
        }

    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "verdict": "runtime_error",
            "results": [],
            "time_ms": 0,
            "error": "Не удалось прочитать результат выполнения",
        }
    finally:
        try:
            out_path.unlink(missing_ok=True)
        except OSError:
            pass

    results = data.get("results", [])
    if any(r.get("error") for r in results):
        verdict = "runtime_error"
    else:
        verdict = "accepted" if all(r.get("passed") for r in results) else "wrong_answer"
    results = [
        {
            "id": r.get("id"),
            "passed": bool(r.get("passed")),
            "expected": _json_safe(r.get("expected")),
            "actual": _json_safe(r.get("actual")),
            "error": r.get("error"),
        }
        for r in results
    ]
    return {
        "verdict": verdict,
        "results": results,
        "time_ms": int(data.get("time_ms", 0)),
        "error": None,
    }