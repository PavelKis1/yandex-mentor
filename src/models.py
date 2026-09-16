"""Pydantic-модели: валидация запросов/ответов на границах API."""
from typing import Literal

from pydantic import BaseModel, Field


# === Roadmap ===


class LectureSummary(BaseModel):
    """Тема (лекция) на роадмапе."""

    id: str
    name: str


class RoadmapStage(BaseModel):
    """Раздел роадмапа (блок тем)."""

    id: str
    name: str
    icon: str
    lectures: list[LectureSummary] = Field(default_factory=list)


class RoadmapResponse(BaseModel):
    """Ответ GET /api/roadmap."""

    roadmap: list[RoadmapStage] = Field(default_factory=list)
    total: int = 0


# === Задачи (problems) ===


class ProblemSummary(BaseModel):
    """Короткое описание задачи для списка (вкладки)."""

    id: str
    title: str
    difficulty: Literal["easy", "medium", "hard"]
    order: int = 1
    solved: bool = False


class ProblemPublic(BaseModel):
    """Открытая часть задачи (без тест-кейсов и ожидаемых ответов)."""

    id: str
    title: str
    difficulty: Literal["easy", "medium", "hard"]
    order: int
    description: str
    examples: list = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    hints: list[str] = Field(default_factory=list)
    starter_code: str = ""
    entry_function: str | None = None
    code: str | None = None  # сохранённое решение пользователя
    test_case_count: int = 0


class LectureData(BaseModel):
    """Ответ GET /api/lectures/{lecture_id}."""

    id: str
    name: str
    stage_id: str
    stage_name: str
    lecture_md: str = ""
    status: Literal["todo", "wip", "done"] = "todo"
    problems: list[ProblemPublic] = Field(default_factory=list)
    
    # НОВЫЕ ОПЦИОНАЛЬНЫЕ ПОЛЯ
    description: str | None = None
    durationMinutes: int | None = None
    difficulty: Literal["junior", "middle", "hard"] | None = None
    tags: list[str] = Field(default_factory=list)
    learningOutcomes: list[str] = Field(default_factory=list)
    complexity: dict | None = None
    quizzes: list[dict] = Field(default_factory=list)
    attachedTasks: list[dict] = Field(default_factory=list)
    cheatSheet: dict | None = None


# === Проверка решений ===


class CodeSubmit(BaseModel):
    """Тело запроса run/submit: пользовательский код."""

    code: str = Field(..., min_length=1, max_length=200_000)


class TestCaseResult(BaseModel):
    """Результат одного тест-кейса."""

    id: str
    passed: bool
    expected: object | None = None
    actual: object | None = None
    error: str | None = None


Verdict = Literal[
    "accepted", "wrong_answer", "runtime_error", "timeout", "syntax_error", "no_tests"
]


class RunResponse(BaseModel):
    """Ответ POST /api/tasks/{problem_id}/run (без скрытых тестов)."""

    problem_id: str
    verdict: Verdict
    results: list[TestCaseResult] = Field(default_factory=list)
    time_ms: int = 0


class SubmitResponse(RunResponse):
    """Ответ POST /api/tasks/{problem_id}/submit (все тесты + статус темы)."""

    task_status: Literal["todo", "wip", "done"] = "wip"


# === Прогресс / статусы ===


class StatusUpdate(BaseModel):
    """Ручная смена статуса темы (todo / wip / done)."""

    status: Literal["todo", "wip", "done"]


class ErrorEvent(BaseModel):
    """Запись ошибки пользователя по задаче."""

    task_id: str
    error: str
    hint: str = ""