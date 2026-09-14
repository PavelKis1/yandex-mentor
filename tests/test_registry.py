"""Тесты реестра: roadmap.json, лекции и задачи backend/tasks/."""
from src.core.registry import (
    build_roadmap,
    find_lecture,
    get_problem,
    list_lectures,
    list_problems,
    list_stages,
    parse_problem_id,
)


def test_roadmap_total_69():
    data = build_roadmap()
    assert data["total"] == 69
    assert len(data["roadmap"]) == 7
    first = data["roadmap"][0]
    assert first["id"] == "algorithms"
    assert len(first["lectures"]) == 25


def test_stages_order():
    stages = list_stages()
    assert [s.id for s in stages] == [
        "algorithms",
        "python",
        "databases",
        "backend",
        "linux",
        "system_design",
        "mocks",
    ]


def test_list_lectures_names():
    lectures = list_lectures()
    assert len(lectures) == 69
    by_id = {lecture.id: lecture for lecture in lectures}
    assert by_id["01"].name == "Хеш-таблицы"
    assert by_id["01"].dir == "01_hash_tables"
    assert by_id["36"].name == "SQL: SELECT"
    assert by_id["66"].name == "Мок: Алгоритм"


def test_find_lecture():
    assert find_lecture("01") is not None
    assert find_lecture("99") is None


def test_list_problems_has_three_per_lecture():
    problems = list_problems("01")
    assert len(problems) == 3
    assert [p.order for p in problems] == [1, 2, 3]
    assert [p.difficulty for p in problems] == ["easy", "medium", "hard"]


def test_get_problem():
    problem = get_problem("01-p1")
    assert problem is not None
    assert problem.entry_function == "two_sum"
    assert problem.test_cases_count() >= 3
    hidden = [c for c in problem.test_cases if c.hidden]
    assert hidden, "у демо-задачи должен быть скрытый тест"
    # отсутствующие задачи
    assert get_problem("99-p1") is None
    assert get_problem("01-p9") is None
    assert get_problem("bogus") is None


def test_problem_parse_id():
    assert parse_problem_id("01-p2") == ("01", 2)
    assert parse_problem_id("nope") is None