"""Миграция контента из старой структуры backend/ в backend/tasks/.

Старая структура:
    backend/{stage}/NN_slug/task.md + task_NN.py + lecture.md

Новая структура (единый каталог задач):
    backend/roadmap.json
    backend/tasks/NN_slug/lecture.md
    backend/tasks/NN_slug/problems/p1.json … pN.json

Что делает скрипт:
  - создаёт backend/roadmap.json (разделы + темы в порядке изучения);
  - переносит lecture.md в backend/tasks/NN_slug/;
  - разбирает task.md в структурированные problems/*.json:
      title, description, examples, hints, difficulty;
  - из task_NN.py (там, где файл валидный) извлекает:
      starter_code (сигнатура + docstring + class/helpers),
      entry_function,
      test_cases (из assert-ов через AST, включая helpers _build/_to_list
      и доступ .val);
  - к каждой лекции доводит число заданий до 3.

Скрипт идемпотентен: папки, которые уже есть в backend/tasks/, не трогает
(перезапись — только с --force).
"""
import argparse
import ast
import json
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "backend"
META_FILE = BASE_DIR / "src" / "core" / "tasks_meta.json"
TASKS_DIR = CONTENT_DIR / "tasks"

# Порядок разделов роадмапа (совпадает с прежним src/core/registry.py::STAGES).
STAGES: list[dict[str, str]] = [
    {"id": "algorithms", "name": "Алгоритмы", "icon": "🧠", "dir": "algorithms"},
    {"id": "python", "name": "Python", "icon": "🐍", "dir": "python"},
    {"id": "databases", "name": "Базы данных", "icon": "🗄️", "dir": "databases"},
    {"id": "backend", "name": "Backend", "icon": "🛠️", "dir": "backend"},
    {"id": "linux", "name": "Linux и Observability", "icon": "🐧", "dir": "linux"},
    {"id": "system_design", "name": "System Design", "icon": "🏗️", "dir": "system_design"},
    {"id": "mocks", "name": "Моки", "icon": "🎯", "dir": "mocks"},
]

PROBLEM_PER_LECTURE = 3
DIFFICULTY_BY_ORDER = ["easy", "medium", "hard"]
MAX_TEST_CASES = 8


def load_meta() -> dict[str, dict]:
    """task_id -> {name, file, skill} из прежнего tasks_meta.json."""
    try:
        data = json.loads(META_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    return data or {}


def split_top_level(text: str, sep: str = ",") -> list[str]:
    """Разбить строку по разделителю вне скобок/кавычек (для 'nums=[1,2], k=2')."""
    parts: list[str] = []
    depth = 0
    quote: str | None = None
    current: list[str] = []
    for ch in text:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            current.append(ch)
            continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    tail = "".join(current).strip()
    if tail:
        parts.append(tail)
    return [p for p in parts if p]


def try_literal(value: str):
    """ast.literal_eval с аккуратной обработкой."""
    value = value.strip()
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def strip_backticks(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1].strip()
    return value


def parse_example_line(line: str) -> dict | None:
    """Разобрать строку вида '**Пример:** `nums=[...] → [...]`' в {input, output}.

    Если в тексте несколько стрелок (например, пример-последовательность) — ответ
    неоднозначен, и пример сохраняем целиком без разбиения (только для показа).
    """
    text = line.replace("**Пример:**", "", 1).strip()
    text = text.strip("-").strip()
    text = strip_backticks(text)
    arrow = text.rfind("→")
    if arrow < 0:
        arrow = text.rfind("->")
    if arrow < 0:
        return {"input": text, "output": "", "explanation": None}
    left = text[:arrow].strip()
    right = text[arrow + 1 :].strip()
    right = right.lstrip("=").strip()
    if not left or not right:
        return {"input": text, "output": "", "explanation": None}
    if "→" in left or "->" in left:
        # Стрелка встречается и левее — это описание последовательности, не контракт.
        return {"input": text, "output": "", "explanation": None}
    return {"input": left, "output": right, "explanation": None}


def parse_problems(task_md: str) -> list[dict]:
    """Разобрать task.md в список {title, description, examples, hints}."""
    problems: list[dict] = []
    parts = re.split(r"^##\s+", task_md, flags=re.MULTILINE)
    for part in parts[1:]:
        lines = part.split("\n")
        heading = lines[0].strip()
        if not re.match(r"^Задание\s*\d", heading, re.IGNORECASE):
            continue
        title = heading
        colon = heading.find(":")
        if colon > 0:
            title = heading[colon + 1 :].strip() or title

        body_lines: list[str] = []
        examples: list[dict] = []
        hints: list[str] = []
        for raw_line in lines[1:]:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("**Пример:**") or line.startswith("Пример:"):
                parsed = parse_example_line(line)
                if parsed is not None:
                    examples.append(parsed)
                continue
            if line.startswith("💡") or line.startswith("**Подсказка:**") or line.startswith("Подсказка"):
                hint = line.split(":", 1)[-1] if ":" in line else line
                hint = hint.strip("💡 ").strip("**").strip()
                if hint:
                    hints.append(hint)
                continue
            body_lines.append(raw_line)

        description = "\n".join(body_lines).strip()
        if not description and examples:
            description = "* Используйте примеры ниже как контракт ввода/вывода."
        problems.append(
            {
                "title": title,
                "description": description,
                "examples": examples,
                "hints": hints,
            }
        )
    return problems[:PROBLEM_PER_LECTURE]
def signatures(tree: ast.Module) -> list[tuple[str, ast.FunctionDef]]:
    """Публичные функции модуля в порядке объявления (без underscore-хелперов)."""
    result: list[tuple[str, ast.FunctionDef]] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            result.append((node.name, node))
    return result


def signature_and_docstring(source: str, node: ast.FunctionDef) -> str:
    """Сигнатура функции + docstring (то, что показываем в starter_code)."""
    lines = source.splitlines(keepends=True)
    first = node.body[0]
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        end_line = first.end_lineno  # захватываем docstring целиком
    else:
        end_line = first.lineno - 1
    return "".join(lines[node.lineno - 1 : end_line]).rstrip()


def build_starter(source: str, tree: ast.Module, entry_name: str | None) -> str:
    """starter_code: импорты + class-ы + entry-сигнатура (с заглушкой) + underscore-хелперы.

    Тело entry-функции не копируется (это и есть задача), поэтому в теле — `...`.
    Полные тексты underscore-функций (конвертеры _build/_to_list) входят целиком:
    без них нельзя запускать тесты с конвертерами.
    """
    parts: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            parts.append(ast.get_source_segment(source, node))
        elif isinstance(node, ast.ClassDef):
            parts.append(ast.get_source_segment(source, node))
        elif isinstance(node, ast.FunctionDef):
            if node.name == entry_name:
                header = signature_and_docstring(source, node)
                parts.append(f"{header}\n    ...")
            elif node.name.startswith("_"):
                parts.append(ast.get_source_segment(source, node))
    starter = "\n\n".join(parts).strip()
    if starter and not starter.endswith("\n"):
        starter += "\n"
    return starter


def lit(value: ast.expr):
    """Безопасный literal_eval для аргументов/ожиданий из assert-ов."""
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def resolve_assert(test: ast.expr, entry: str) -> dict | None:
    """Превратить assert-выражение в {args, arg_converters, result_converter, expected}.

    Поддерживаемые формы (проверяются именно для entry-функции):
      entry(*literal_args) ==/is literal
      _to_list(entry(args)) == literal
      entry(...).val == literal
    """
    if not isinstance(test, ast.Compare) or len(test.comparators) != 1:
        return None
    op = test.ops[0]

    if isinstance(op, (ast.Is, ast.IsNot)):
        expected = None
        comp = test.comparators[0]
        if isinstance(comp, ast.Constant):
            expected = comp.value
    elif isinstance(op, ast.Eq):
        expected = lit(test.comparators[0])
    else:
        return None
    if expected is None and not isinstance(test.comparators[0], ast.Constant):
        # literal_eval вернул None из-за ошибки парсинга — пропускаем
        return None

    left = test.left
    result_converter: str | None = None

    # а) entry(*args) == literal
    if isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and left.func.id == entry:
        call = left
        extract_attr = None
    # б) _to_list(entry(args)) == literal
    elif (
        isinstance(left, ast.Call)
        and isinstance(left.func, ast.Name)
        and left.func.id.startswith("_")
        and left.args
        and isinstance(left.args[0], ast.Call)
        and isinstance(left.args[0].func, ast.Name)
        and left.args[0].func.id == entry
    ):
        result_converter = left.func.id
        call = left.args[0]
        extract_attr = None
    # в) entry(...).val == literal
    elif (
        isinstance(left, ast.Attribute)
        and isinstance(left.value, ast.Call)
        and isinstance(left.value.func, ast.Name)
        and left.value.func.id == entry
        and isinstance(left.attr, str)
    ):
        extract_attr = left.attr
        call = left.value
    else:
        return None

    args: list = []
    arg_converters: list[str | None] = []
    for arg in call.args:
        if (
            isinstance(arg, ast.Call)
            and isinstance(arg.func, ast.Name)
            and arg.func.id.startswith("_")
            and len(arg.args) == 1
        ):
            value = lit(arg.args[0])
            if value is None:
                return None
            args.append(value)
            arg_converters.append(arg.func.id)
        else:
            value = lit(arg)
            if value is None:
                return None
            args.append(value)
            arg_converters.append(None)

    if extract_attr:
        result_converter = f"attr:{extract_attr}"
    return {
        "args": args,
        "arg_converters": arg_converters,
        "result_converter": result_converter,
        "expected": expected,
    }


def cases_from_asserts(source: str, tree: ast.Module, entry: str) -> list[dict]:
    """test_cases из assert-блоков файла решения (с конвертерами _build/_to_list)."""
    cases: list[dict] = []
    seen: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assert):
            continue
        converted = resolve_assert(node.test, entry)
        if converted is None:
            continue
        key = json.dumps(converted, ensure_ascii=False, sort_keys=True)
        if key in seen:
            continue
        seen.add(key)
        cases.append(
            {
                "id": f"t{len(cases) + 1}",
                "args": converted["args"],
                "expected": converted["expected"],
                "hidden": False,
                "arg_converters": converted["arg_converters"],
                "result_converter": converted["result_converter"],
            }
        )
        if len(cases) >= MAX_TEST_CASES:
            break
    return cases


def cases_from_examples(problems: list[dict], entry_node: ast.FunctionDef | None) -> list[dict]:
    """test_cases из примеров task.md для тем без assert-ов (по именам параметров)."""
    if entry_node is None:
        return []
    param_names = [a.arg for a in entry_node.args.args]
    cases: list[dict] = []
    seen: set[str] = set()
    for problem in problems:
        for example in problem.get("examples", []):
            values: dict[str, object] = {}
            ok = True
            for segment in split_top_level(example["input"]):
                if "=" not in segment:
                    ok = False
                    break
                name, _, raw = segment.partition("=")
                name = name.strip()
                raw = strip_backticks(raw.strip())
                if not re.fullmatch(r"[A-Za-z_]\w*", name):
                    ok = False
                    break
                value = try_literal(raw)
                if value is None:
                    ok = False
                    break
                values[name] = value
            if not ok:
                continue
            expected = try_literal(example["output"])
            if expected is None:
                continue
            if not all(name in values for name in param_names):
                continue
            args = [values[name] for name in param_names]
            key = json.dumps({"a": args, "e": expected}, ensure_ascii=False)
            if key in seen:
                continue
            seen.add(key)
            cases.append(
                {
                    "id": f"t{len(cases) + 1}",
                    "args": args,
                    "expected": expected,
                    "hidden": False,
                    "arg_converters": [None] * len(args),
                    "result_converter": None,
                }
            )
            if len(cases) >= MAX_TEST_CASES:
                break
    return cases


def pad_problems(problems: list[dict]) -> list[dict]:
    """Доводим число заданий лекции до 3 (по требованию продукта)."""
    padded = list(problems)
    while len(padded) < PROBLEM_PER_LECTURE:
        n = len(padded) + 1
        padded.append(
            {
                "title": f"Дополнительная практика №{n}",
                "description": "Примените материал лекции на практике: придумайте свою "
                "задачу по теме и решите её. Опишите условие, решение и проверьте "
                "на нескольких примерах.\n\n"
                "*Это дополняющее задание — основной материал лекции уже покрыт "
                "заданиями выше.",
                "examples": [],
                "hints": [],
            }
        )
    return padded


def contract_block(entry_name: str | None, starter_part: str) -> str:
    """Блок «Контракт решения» для текста задания."""
    if not entry_name:
        return ""
    fence = "```"
    return f"\n\n**Функция решения:**\n\n{fence}python\n{starter_part}\n{fence}"


def migrate_topic(topic_dir: Path, task_id: str, meta_entry: dict, force: bool) -> int:
    """Мигрировать одну тему; вернуть количество написанных problems (0 если пропущена)."""
    target_dir = TASKS_DIR / topic_dir.name

    if target_dir.exists() and not force:
        return 0

    # ---- 1. Решение (task_NN.py) ----
    solution_file = topic_dir / (meta_entry.get("file") or f"task_{task_id}.py")
    source: str | None = None
    tree: ast.Module | None = None
    funcs: list[tuple[str, ast.FunctionDef]] = []
    if solution_file.exists():
        try:
            source = solution_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception:
            source = None
        if tree is not None:
            funcs = signatures(tree)

    # ---- 2. task.md ----
    task_md_path = topic_dir / "task.md"
    task_md = task_md_path.read_text(encoding="utf-8-sig") if task_md_path.exists() else ""
    problems = parse_problems(task_md) if task_md else []
    problems = pad_problems(problems)

    # ---- 3. Лекция ----
    if target_dir.exists():
        shutil.rmtree(target_dir)
    (target_dir / "problems").mkdir(parents=True, exist_ok=True)
    lecture_src = topic_dir / "lecture.md"
    if lecture_src.exists():
        shutil.copy2(lecture_src, target_dir / "lecture.md")

    # ---- 4. Каждое задание -> problems/pN.json ----
    for index, problem in enumerate(problems, start=1):
        entry_name: str | None = None
        entry_node: ast.FunctionDef | None = None
        if index <= len(funcs):
            entry_name, entry_node = funcs[index - 1]

        starter = ""
        test_cases: list[dict] = []
        if tree is not None and entry_name:
            starter = build_starter(source, tree, entry_name) if source else ""
            test_cases = cases_from_asserts(source, tree, entry_name)
            if not test_cases:
                test_cases = cases_from_examples(problems, entry_node)

        description = problem["description"]
        if entry_name and source and entry_node:
            header = signature_and_docstring(source, entry_node)
            description += contract_block(entry_name, header)

        data = {
            "id": f"{task_id}-p{index}",
            "title": problem["title"],
            "difficulty": DIFFICULTY_BY_ORDER[index - 1],
            "lecture_id": task_id,
            "order": index,
            "description": description,
            "examples": problem["examples"],
            "constraints": [],
            "hints": problem["hints"],
            "starter_code": starter,
            "entry_function": entry_name,
            "test_cases": test_cases,
            "timeout_ms": 3000,
        }
        (target_dir / "problems" / f"p{index}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ---- 5. Старые файлы удаляются (бэкап уже сделан) ----
    for old in ("task.md", solution_file.name):
        old_path = topic_dir / old
        if old_path.exists():
            try:
                old_path.unlink()
            except OSError:
                pass
    return len(problems)


def main(force: bool = False, delete_source: bool = True) -> None:
    """Основной поток миграции: roadmap.json + backend/tasks/NN_slug/*."""
    meta = load_meta()
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    roadmap_stages: list[dict] = []
    total = 0
    problems_written = 0
    skipped: list[str] = []

    for stage in STAGES:
        stage_block: Path = CONTENT_DIR / stage["dir"]
        lectures: list[dict] = []
        if not stage_block.is_dir():
            roadmap_stages.append(
                {
                    "id": stage["id"],
                    "name": stage["name"],
                    "icon": stage["icon"],
                    "lectures": lectures,
                }
            )
            continue

        for topic_dir in sorted(stage_block.iterdir()):
            if not topic_dir.is_dir():
                continue
            match = re.match(r"^(\d{2})_", topic_dir.name)
            if match is None:
                continue
            task_id = match.group(1)
            meta_entry = meta.get(task_id, {})
            name = meta_entry.get("name") or topic_dir.name

            if TASKS_DIR.joinpath(topic_dir.name).exists() and not force:
                skipped.append(topic_dir.name)
                lectures.append({"id": task_id, "name": name, "dir": topic_dir.name})
                total += 1
                continue

            written = migrate_topic(topic_dir, task_id, meta_entry, force)
            problems_written += written
            total += 1
            lectures.append({"id": task_id, "name": name, "dir": topic_dir.name})

        roadmap_stages.append(
            {"id": stage["id"], "name": stage["name"], "icon": stage["icon"], "lectures": lectures}
        )

    (CONTENT_DIR / "roadmap.json").write_text(
        json.dumps({"stages": roadmap_stages, "total": total}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Итоговая статистика: сколько задач имеют автопроверку
    with_tests = 0
    all_problems = 0
    for problem_file in sorted(TASKS_DIR.glob("*/problems/p*.json")):
        try:
            cfg = json.loads(problem_file.read_text(encoding="utf-8"))
            all_problems += 1
            if cfg.get("test_cases"):
                with_tests += 1
        except (OSError, json.JSONDecodeError):
            pass

    print("=" * 72)
    print(f"Миграция завершена: лекции={total}, problems={problems_written}")
    print(f"test_cases автогенерированы для {with_tests} из {all_problems} задач")
    print(f"пропущены (уже мигрированы): {len(skipped)}")
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Миграция контента в backend/tasks/")
    parser.add_argument("--force", action="store_true", help="перезаписать существующие задачи")
    parser.add_argument("--keep-source", action="store_true", help="не удалять task.md/task_NN.py")
    args = parser.parse_args()
    main(force=args.force, delete_source=not args.keep_source)