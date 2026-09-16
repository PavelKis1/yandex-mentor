"""Тесты REST API: лекции, задачи, run/submit, статусы."""
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src import config
from src.api.routes import router

TWO_SUM_CODE = """\
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        c = target - x
        if c in seen:
            return [seen[c], i]
        seen[x] = i
    return []
"""

GROUP_ANAGRAMS_CODE = """\
def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)
    return list(groups.values())
"""

COUNT_SUBSETS_CODE = """\
def count_subsets(nums, target):
    dp = {0: 1}
    for x in nums:
        new = dict(dp)
        for s, c in dp.items():
            new[s + x] = new.get(s + x, 0) + c
        dp = new
    return dp.get(target, 0)
"""


def _make_client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setattr(config, "PROGRESS_FILE", tmp_path / "progress.json")
    monkeypatch.setattr(config, "SOLVED_FILE", tmp_path / "solved.json")
    monkeypatch.setattr(config, "ERRORS_FILE", tmp_path / "errors.json")
    monkeypatch.setattr(config, "SOLUTIONS_DIR", tmp_path / "solutions")
    (tmp_path / "solutions").mkdir(exist_ok=True)
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_roadmap(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    body = client.get("/api/roadmap").json()
    assert body["total"] == 69
    assert len(body["roadmap"]) == 7


def test_progress_empty(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    assert client.get("/api/progress").json() == {}


def test_get_lecture(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    body = client.get("/api/lectures/01").json()
    assert body["name"] == "Хеш-таблицы"
    assert body["stage_id"] == "algorithms"
    assert len(body["problems"]) == 3
    first = body["problems"][0]
    assert first["id"] == "01-p1"
    assert first["entry_function"] == "two_sum"
    assert "test_cases" not in first  # тесты не отдаются наружу
    assert first["test_case_count"] == 5


def test_get_lecture_meta(tmp_path, monkeypatch):
    """Опциональные метаданные из lecture.meta.json аддитивно добавляются в ответ."""
    import pathlib

    meta_path = (
        pathlib.Path(config.BASE_DIR)
        / "backend"
        / "tasks"
        / "01_hash_tables"
        / "lecture.meta.json"
    )
    meta_path.write_text(
        json.dumps(
            {
                "description": "Вводная лекция",
                "difficulty": "junior",
                "durationMinutes": 25,
                "tags": ["hash", "intro"],
                "learningOutcomes": ["Решать задачи с Two Sum"],
                "attachedTasks": [{"taskId": "01-p1", "title": "Two Sum"}],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    try:
        client = _make_client(tmp_path, monkeypatch)
        body = client.get("/api/lectures/01").json()
        assert body["description"] == "Вводная лекция"
        assert body["difficulty"] == "junior"
        assert body["durationMinutes"] == 25
        assert body["tags"] == ["hash", "intro"]
        assert body["learningOutcomes"] == ["Решать задачи с Two Sum"]
        assert body["attachedTasks"][0]["taskId"] == "01-p1"
        # поля по умолчанию для аддитивности
        assert body["quizzes"] == []
    finally:
        meta_path.unlink(missing_ok=True)


def test_get_lecture_without_meta(tmp_path, monkeypatch):
    """Без lecture.meta.json ответ содержит те же поля с пустыми значениями (обратная совместимость)."""
    client = _make_client(tmp_path, monkeypatch)
    body = client.get("/api/lectures/01").json()
    assert body.get("description") is None
    assert body.get("difficulty") is None
    assert body.get("tags") == []
    assert body.get("attachedTasks") == []
    assert body.get("quizzes") == []
def test_get_lecture_404(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    assert client.get("/api/lectures/99").status_code == 404


def test_run_accepted_public_only(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    body = client.post(
        "/api/tasks/01-p1/run", json={"code": TWO_SUM_CODE}
    ).json()
    assert body["verdict"] == "accepted"
    assert len(body["results"]) == 4  # скрытый t5 не выполняется


def test_submit_one_problem_not_done(tmp_path, monkeypatch):
    """Баг-фикс: решение ОДНОЙ задачи из трёх не делает лекцию done."""
    client = _make_client(tmp_path, monkeypatch)
    body = client.post(
        "/api/tasks/01-p1/submit", json={"code": TWO_SUM_CODE}
    ).json()
    assert body["verdict"] == "accepted"
    assert body["task_status"] == "wip"
    assert client.get("/api/progress").json()["01"] == "wip"
    # задача отмечена как решённая, лекция — нет
    lecture = client.get("/api/lectures/01").json()
    assert lecture["problems"][0]["solved"] is True
    assert lecture["status"] == "wip"


def test_submit_all_problems_marks_done(tmp_path, monkeypatch):
    """Лекция становится done только после решения ВСЕХ её задач."""
    client = _make_client(tmp_path, monkeypatch)
    for problem_id, code in (
        ("01-p1", TWO_SUM_CODE),
        ("01-p2", GROUP_ANAGRAMS_CODE),
        ("01-p3", COUNT_SUBSETS_CODE),
    ):
        body = client.post(f"/api/tasks/{problem_id}/submit", json={"code": code}).json()
        assert body["verdict"] == "accepted", f"{problem_id}: {body}"
    assert client.get("/api/progress").json()["01"] == "done"
    # плашки «решено» восстановлены для всех задач лекции
    lecture = client.get("/api/lectures/01").json()
    assert lecture["status"] == "done"
    assert all(p["solved"] for p in lecture["problems"])


def test_submit_after_done_keeps_done(tmp_path, monkeypatch):
    """Повторный неверный сабмит не «откатывает» уже решённую тему."""
    client = _make_client(tmp_path, monkeypatch)
    for problem_id, code in (
        ("01-p1", TWO_SUM_CODE),
        ("01-p2", GROUP_ANAGRAMS_CODE),
        ("01-p3", COUNT_SUBSETS_CODE),
    ):
        client.post(f"/api/tasks/{problem_id}/submit", json={"code": code})
    wrong = client.post(
        "/api/tasks/01-p1/submit",
        json={"code": "def two_sum(nums, target):\n    return [0, 0]\n"},
    ).json()
    assert wrong["verdict"] == "wrong_answer"
    assert client.get("/api/progress").json()["01"] == "done"


def test_submit_wrong_answer_marks_wip(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    body = client.post(
        "/api/tasks/01-p1/submit", json={"code": "def two_sum(nums, target):\n    return [0,0]\n"}
    ).json()
    assert body["verdict"] == "wrong_answer"
    assert body["task_status"] == "wip"


def test_submit_updates_lecture_data(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    client.post("/api/tasks/01-p1/submit", json={"code": TWO_SUM_CODE})
    lecture = client.get("/api/lectures/01").json()
    problem = lecture["problems"][0]
    assert problem["code"] == TWO_SUM_CODE


def test_no_tests_verdict(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    body = client.post("/api/tasks/60-p1/run", json={"code": "anything"}).json()
    assert body["verdict"] == "no_tests"


def test_unknown_problem_404(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    resp = client.post("/api/tasks/99-p1/run", json={"code": "x"})
    assert resp.status_code == 404
    resp = client.get("/api/tasks/01-p9")
    assert resp.status_code == 404


def test_status_flow(tmp_path, monkeypatch):
    client = _make_client(tmp_path, monkeypatch)
    resp = client.post("/api/task/01/status", json={"status": "wip"})
    assert resp.status_code == 200
    assert client.get("/api/progress").json()["01"] == "wip"
    assert client.post("/api/task/99/status", json={"status": "todo"}).status_code == 404
    assert client.post("/api/task/01/status", json={"status": "bogus"}).status_code == 422