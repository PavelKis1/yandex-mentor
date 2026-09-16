"""Генератор «золотого стандарта» для блоков 13-25.

Вычисляет expected для каждого теста вызовом эталонной функции из ref_check,
что гарантирует совпадение при прогоне scripts/ref_check.py.

Запуск: python scripts/_gen/genlib.py
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ref_check  # эталонные функции и REF

BASE = Path(__file__).resolve().parent.parent.parent / "backend" / "tasks"

REF = ref_check.REF


def build_problem(entry, args_list, hidden_flags=None):
    """Cобираем pN.json: expected берётся как эталонный результат."""
    if entry.get("wrap_single"):
        args_list = [[a] for a in args_list]
    fn = REF[entry["id"]]
    tests = []
    for i, args in enumerate(args_list):
        # Эталон может мутировать вход (напр. «затапливать» острова),
        # поэтому считаем результат на глубокой копии, а в тест кладём оригинал.
        got = fn(*copy.deepcopy(args))
        hidden = bool(hidden_flags[i]) if hidden_flags else False
        tests.append({
            "id": f"t{i + 1}",
            "args": args,
            "expected": got,
            "hidden": hidden,
            "arg_converters": [None] * len(args),
            "result_converter": None,
        })
    prob = {
        "id": entry["id"],
        "title": entry["title"],
        "difficulty": entry["difficulty"],
        "lecture_id": entry["lecture_id"],
        "order": entry["order"],
        "description": entry["description"],
        "examples": entry["examples"],
        "constraints": entry["constraints"],
        "hints": entry["hints"],
        "starter_code": entry["starter_code"],
        "entry_function": entry["entry_function"],
        "test_cases": tests,
        "timeout_ms": 3000,
    }
    return prob


def write_problem(entry, args_list, hidden_flags=None):
    prob = build_problem(entry, args_list, hidden_flags)
    folder = BASE / entry["lecture_slug"]
    folder.mkdir(parents=True, exist_ok=True)
    pdir = folder / "problems"
    pdir.mkdir(exist_ok=True)
    pdir.joinpath(f"p{entry['order']}.json").write_text(
        json.dumps(prob, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(prob["test_cases"])


def write_meta(meta):
    folder = BASE / meta["lecture_slug"]
    folder.joinpath("lecture.meta.json").write_text(
        json.dumps(meta["data"], ensure_ascii=False, indent=2), encoding="utf-8")


def run(blocks):
    total_tests = 0
    for block in blocks:
        write_meta(block)
        for entry in block["problems"]:
            n = write_problem(entry, entry["args"], entry.get("hidden"))
            total_tests += n
        print(f"{block['data']['id']:>2} {block['data']['slug']:<24} done")
    print(f"Итого тест-кейсов: {total_tests}")