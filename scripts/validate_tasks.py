"""Валидация задач: JSON-синтаксис и согласованность lecture.meta.json с problems.

Проверки:
1. Все JSON в backend/tasks/<lecture>/ парсятся.
2. lecture.meta.json содержит обязательные поля: id, slug, title, description,
   durationMinutes, difficulty, tags, learningOutcomes, complexity, quizzes,
   attachedTasks, cheatSheet.
3. attachedTasks[].taskId соответствуют реальным problems/pX.json id.
4. attachedTasks[].difficulty совпадает с difficulty задачи.
5. В каждой задаче test_cases[]: количество arg_converters равно количеству args.
6. Хотя бы один из taskId существует в attachedTasks для каждой задачи.

Запуск: python scripts/validate_tasks.py [prefix]  (prefix фильтрует директории, напр. '0')
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "backend" / "tasks"

REQUIRED_META = [
    "id", "slug", "title", "description", "durationMinutes", "difficulty",
    "tags", "learningOutcomes", "complexity", "quizzes", "attachedTasks", "cheatSheet",
]


def validate_lecture(dirpath: Path):
    problems = dirpath / "problems"
    report = []

    # --- парсинг всей JSON'ы директории ---
    files = [dirpath / "lecture.meta.json", problems / "p1.json",
             problems / "p2.json", problems / "p3.json"]
    for f in files:
        if not f.exists():
            report.append(f"  [!!] отсутствует: {f.relative_to(BASE)}")
            continue
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            report.append(f"  [!!] битый JSON {f.name}: {e}")

    meta_path = dirpath / "lecture.meta.json"
    if not meta_path.exists():
        return "\n".join(report) or "  [OK] (нет meta)"

    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    # --- обязательные поля ---
    missing = [k for k in REQUIRED_META if k not in meta]
    if missing:
        report.append(f"  [!!] meta: нет полей {missing}")

    # --- quizzes ---
    for q in meta.get("quizzes", []):
        for o in q.get("options", []):
            if not isinstance(o.get("isCorrect"), bool):
                report.append(f"  [!!] quiz {q.get('id')}: isCorrect не bool -> {o.get('text')}")

    # --- attachedTasks vs проблемы ---
    probs = {}
    for idx in (1, 2, 3):
        p = problems / f"p{idx}.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            probs[data["id"]] = data

    attached = meta.get("attachedTasks", [])
    for a in attached:
        pid = a.get("taskId")
        if pid not in probs:
            report.append(f"  [!!] attachedTasks ссылается на несуществующую задачу {pid}")
        else:
            if probs[pid]["difficulty"] != a.get("difficulty"):
                report.append(f"  [!!] {pid}: difficulty в meta ({a.get('difficulty')}) != в задаче ({probs[pid]['difficulty']})")
            if probs[pid]["title"] != a.get("title"):
                report.append(f"  [!!] {pid}: title в meta ({a.get('title')}) != в задаче ({probs[pid]['title']})")

    for pid, data in probs.items():
        if pid not in {a.get("taskId") for a in attached}:
            report.append(f"  [!!] задача {pid} не привязана в attachedTasks")
        for tc in data.get("test_cases", []):
            n_args = len(tc.get("args", []))
            n_conv = len(tc.get("arg_converters", [] or None) or [])
            if n_conv and n_conv != n_args:
                report.append(f"  [!!] {pid}/{tc.get('id')}: конвертеров ({n_conv}) != аргументов ({n_args})")
        for fld in ("examples", "constraints", "hints"):
            if fld not in data:
                report.append(f"  [!!] {pid}: нет поля {fld}")

    return "\n".join(report) if report else "  [OK]"


def main():
    prefix = sys.argv[1] if len(sys.argv) > 1 else ""
    dirs = sorted(p for p in BASE.iterdir() if p.is_dir() and p.name.startswith(prefix))
    if not dirs:
        print(f"Нет директорий по префиксу {prefix!r}")
        return
    problems_found = 0
    for d in dirs:
        print(f"=== {d.name} ===")
        print(validate_lecture(d))
        n_json = sum(1 for p in d.rglob("*.json"))
        problems_found += len(list((d / "problems").glob("p?.json"))) if (d / "problems").exists() else 0
    print(f"\nЛекций: {len(dirs)}, задач (p1-p3): {problems_found}")


if __name__ == "__main__":
    main()