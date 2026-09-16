"""Реестр задач.

Единый источник правды о структуре учебного плана:
- backend/roadmap.json     — разделы (stages) и темы (lectures) в порядке изучения;
- backend/tasks/NN_slug/   — каталог темы: lecture.md + problems/pN.json.

Каждая задача — это problems/pN.json со схемой:
    id, title, difficulty, lecture_id, order, description, examples,
    constraints, hints, starter_code, entry_function,
    test_cases[{id, args, expected, hidden, arg_converters, result_converter}],
    timeout_ms
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src import config


# === Структуры данных ===


@dataclass(frozen=True)
class Stage:
    """Раздел роадмапа."""

    id: str
    name: str
    icon: str


@dataclass(frozen=True)
class LectureRef:
    """Запись темы в roadmap."""

    id: str
    name: str
    dir: str
    stage_id: str
    stage_name: str


@dataclass
class TestCase:
    """Один тест-кейс задачи."""

    id: str
    args: list
    expected: Any
    hidden: bool = False
    arg_converters: list[str | None] | None = None
    result_converter: str | None = None
    sort_result: bool = False
    # SQL-режим: полный DDL+DML скрипт, создающий БД для этого кейса.
    db_schema: str | None = None
    # Какие колонки ожидаются в результате (имена); иначе — без подписей.
    columns: list[str] | None = None


@dataclass
class Problem:
    """Задача (одна из problems/pN.json)."""

    id: str
    title: str
    difficulty: str
    lecture_id: str
    order: int
    description: str
    examples: list = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)
    starter_code: str = ""
    entry_function: str | None = None
    test_cases: list[TestCase] = field(default_factory=list)
    timeout_ms: int = 3000
    # "python" (по умолчанию) или "sql" — выполнение SQL через sqlite3.
    language: str = "python"
    path: Path | None = None

    def test_cases_count(self) -> int:
        return len(self.test_cases)


# === Чтение roadmap.json ===


def load_roadmap() -> list[dict]:
    """Сырое содержимое roadmap.json (stages) или пустой список."""
    try:
        data = json.loads(config.ROADMAP_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return data.get("stages", []) if isinstance(data, dict) else []


def list_stages() -> list[Stage]:
    return [
        Stage(id=st["id"], name=st.get("name", st["id"]), icon=st.get("icon", "📘"))
        for st in load_roadmap()
    ]


def _lecture_dirs() -> dict[str, Path]:
    """lecture_id -> каталог backend/tasks/NN_slug (по префиксу NN_)."""
    result: dict[str, Path] = {}
    if not config.TASKS_DIR.is_dir():
        return result
    for entry in config.TASKS_DIR.iterdir():
        if not entry.is_dir():
            continue
        match = re.match(r"^(\d{2})_", entry.name)
        if match:
            result[match.group(1)] = entry
    return result


def list_lectures() -> list[LectureRef]:
    """Все темы в порядке роадмапа (id, name, dir, stage)."""
    lectures: list[LectureRef] = []
    dirs = _lecture_dirs()
    for stage in load_roadmap():
        for lec in stage.get("lectures", []):
            lec_id = str(lec.get("id", ""))
            lec_dir = dirs.get(lec_id)
            lectures.append(
                LectureRef(
                    id=lec_id,
                    name=lec.get("name", lec_id),
                    dir=lec_dir.name if lec_dir else "",
                    stage_id=stage.get("id", ""),
                    stage_name=stage.get("name", ""),
                )
            )
    return lectures


def find_lecture(lecture_id: str) -> LectureRef | None:
    for lecture in list_lectures():
        if lecture.id == lecture_id:
            return lecture
    return None


def build_roadmap() -> dict:
    """Ответ GET /api/roadmap: разделы с темами (без задач)."""
    stages = []
    for stage in load_roadmap():
        stages.append(
            {
                "id": stage["id"],
                "name": stage.get("name", stage["id"]),
                "icon": stage.get("icon", "📘"),
                "lectures": [
                    {"id": lec["id"], "name": lec.get("name", lec["id"])}
                    for lec in stage.get("lectures", [])
                ],
            }
        )
    return {"roadmap": stages, "total": sum(len(s.get("lectures", [])) for s in stages)}


# === Задачи (problems) ===


def _parse_test_cases(raw: list[dict]) -> list[TestCase]:
    cases: list[TestCase] = []
    for item in raw or []:
        cases.append(
            TestCase(
                id=str(item.get("id", f"t{len(cases) + 1}")),
                args=item.get("args", []),
                expected=item.get("expected"),
                hidden=bool(item.get("hidden", False)),
                arg_converters=item.get("arg_converters"),
                result_converter=item.get("result_converter"),
                sort_result=bool(item.get("sort_result", False)),
                db_schema=item.get("db_schema"),
                columns=item.get("columns"),
            )
        )
    return cases


def _parse_problem(path: Path) -> Problem | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return Problem(
        id=str(data.get("id", path.stem)),
        title=str(data.get("title", path.stem)),
        difficulty=str(data.get("difficulty", "medium")),
        lecture_id=str(data.get("lecture_id", "")),
        order=int(data.get("order", 1)),
        description=str(data.get("description", "")),
        examples=data.get("examples", []),
        constraints=[str(x) for x in data.get("constraints", [])],
        hints=[str(x) for x in data.get("hints", [])],
        starter_code=str(data.get("starter_code", "")) or "",
        entry_function=data.get("entry_function") or None,
        test_cases=_parse_test_cases(data.get("test_cases", [])),
        timeout_ms=int(data.get("timeout_ms", 3000)),
        language=str(data.get("language", "python") or "python"),
        path=path,
    )


def list_problems(lecture_id: str) -> list[Problem]:
    """Задачи лекции в порядке (p1, p2, p3)."""
    lecture = find_lecture(lecture_id)
    if lecture is None or not lecture.dir:
        return []
    problems_dir = config.TASKS_DIR / lecture.dir / "problems"
    if not problems_dir.is_dir():
        return []
    problems: list[Problem] = []
    for path in sorted(problems_dir.glob("p*.json")):
        problem = _parse_problem(path)
        if problem is not None:
            problems.append(problem)
    return sorted(problems, key=lambda p: p.order)


def parse_problem_id(problem_id: str) -> tuple[str, int] | None:
    """'01-p2' -> ('01', 2)."""
    match = re.fullmatch(r"(\d{2})-p(\d+)", problem_id)
    if match is None:
        return None
    return match.group(1), int(match.group(2))


def get_problem(problem_id: str) -> Problem | None:
    """Найти задачу по id ('01-p1')."""
    parsed = parse_problem_id(problem_id)
    if parsed is None:
        return None
    lecture_id, order = parsed
    for problem in list_problems(lecture_id):
        if problem.order == order:
            return problem
    return None