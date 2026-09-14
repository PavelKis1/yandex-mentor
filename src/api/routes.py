"""REST API: роадмап, лекции, задачи, проверка решений, прогресс."""
from datetime import datetime

from fastapi import APIRouter, HTTPException

from src import config
from src.core import registry
from src.core.checker import run_checks
from src.core.registry import Problem
from src.core.storage import read_json, read_solution, save_solution, write_json
from src.models import CodeSubmit, StatusUpdate

router = APIRouter()


def _problem_public(problem: Problem, solved: bool = False) -> dict:
    """Открытое представление задачи: без тестов и ожидаемых ответов."""
    return {
        "id": problem.id,
        "title": problem.title,
        "difficulty": problem.difficulty,
        "order": problem.order,
        "description": problem.description,
        "examples": problem.examples,
        "constraints": problem.constraints,
        "hints": problem.hints,
        "starter_code": problem.starter_code,
        "entry_function": problem.entry_function,
        "code": read_solution(problem.id),
        "test_case_count": problem.test_cases_count(),
        "solved": solved,
    }


def _update_progress(lecture_id: str, status: str) -> None:
    progress = read_json(config.PROGRESS_FILE)
    progress[lecture_id] = status
    write_json(config.PROGRESS_FILE, progress)


# === Roadmap / Progress ===


@router.get("/api/roadmap")
def get_roadmap():
    """Структура учебного плана: разделы + темы (без заданий)."""
    return registry.build_roadmap()


@router.get("/api/progress")
def get_progress():
    """Статусы всех тем: todo / wip / done (ключ — id лекции)."""
    return read_json(config.PROGRESS_FILE)


@router.post("/api/task/{lecture_id}/status")
def set_task_status(lecture_id: str, body: StatusUpdate):
    """Ручная смена статуса темы (todo / wip / done) с карточки роадмапа."""
    if registry.find_lecture(lecture_id) is None:
        raise HTTPException(status_code=404, detail="Lecture not found")
    _update_progress(lecture_id, body.status)
    return {"task_id": lecture_id, "status": body.status}


# === Лекции и задачи ===


@router.get("/api/lectures/{lecture_id}")
def get_lecture(lecture_id: str):
    """Лекция + все её задачи (описание, examples, starter_code, сохранённый код)."""
    lecture = registry.find_lecture(lecture_id)
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")

    progress = read_json(config.PROGRESS_FILE)
    status = progress.get(lecture_id, "todo")
    problems = registry.list_problems(lecture_id)
    if not problems:
        raise HTTPException(status_code=404, detail="Lecture has no problems")

    lecture_md = ""
    if lecture.dir:
        lecture_file = config.TASKS_DIR / lecture.dir / "lecture.md"
        if lecture_file.exists():
            try:
                lecture_md = lecture_file.read_text(encoding="utf-8")
            except OSError:
                lecture_md = ""

    return {
        "id": lecture.id,
        "name": lecture.name,
        "stage_id": lecture.stage_id,
        "stage_name": lecture.stage_name,
        "lecture_md": lecture_md,
        "status": status,
        "problems": [_problem_public(p) for p in problems],
    }


def _get_problem_or_404(problem_id: str) -> Problem:
    problem = registry.get_problem(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.get("/api/tasks/{problem_id}")
def get_task(problem_id: str):
    """Открытая информация о задаче + сохранённое решение."""
    problem = _get_problem_or_404(problem_id)
    return _problem_public(problem)


# === Проверка решений ===


@router.post("/api/tasks/{problem_id}/run")
def run_task(problem_id: str, body: CodeSubmit):
    """Запустить решение на открытых примерах (без скрытых тестов)."""
    problem = _get_problem_or_404(problem_id)
    result = run_checks(problem, body.code, hide_hidden=True)
    return {"problem_id": problem_id, **result}


@router.post("/api/tasks/{problem_id}/submit")
def submit_task(problem_id: str, body: CodeSubmit):
    """Сдать решение: все тесты (включая скрытые) + обновление прогресса темы."""
    problem = _get_problem_or_404(problem_id)
    result = run_checks(problem, body.code, hide_hidden=False)

    save_solution(problem_id, body.code)

    task_status = "done" if result["verdict"] == "accepted" else "wip"
    _update_progress(problem.lecture_id, task_status)

    return {
        "problem_id": problem_id,
        **result,
        "task_status": task_status,
        "lecture_id": problem.lecture_id,
    }


@router.post("/api/tasks/{problem_id}/code")
def save_task_code(problem_id: str, body: CodeSubmit):
    """Сохранить черновик кода (без проверки тестами)."""
    _get_problem_or_404(problem_id)
    save_solution(problem_id, body.code)
    return {"status": "saved", "problem_id": problem_id}


# === Ошибки пользователя ===


@router.get("/api/errors")
def get_errors():
    """Записанные ранее ошибки по задачам."""
    return read_json(config.ERRORS_FILE)


@router.post("/api/errors")
def add_error(error_data: dict):
    """Добавить ошибку по задаче (дедупликация по тексту)."""
    errors = read_json(config.ERRORS_FILE)
    task_id = error_data.get("task_id")
    error_text = error_data.get("error")
    hint = error_data.get("hint", "")

    if not task_id or not error_text:
        raise HTTPException(status_code=400, detail="task_id and error required")

    task_errors = errors.setdefault(task_id, [])
    if any(item.get("error") == error_text for item in task_errors):
        return {"status": "already_exists"}

    task_errors.append(
        {"error": error_text, "hint": hint, "date": datetime.now().strftime("%Y-%m-%d")}
    )
    write_json(config.ERRORS_FILE, errors)
    return {"status": "added"}


# === Service ===


@router.get("/")
def root():
    """Информация об API."""
    return {
        "message": "Yandex Review API — LeetCode-style проверка решений",
        "docs": "/docs",
        "frontend": "http://localhost:5173",
    }