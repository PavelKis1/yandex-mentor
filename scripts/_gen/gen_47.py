"""Данные блока 47: SQLAlchemy."""
from genlib import run

LECTURE_SLUG = "47_sqlalchemy"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "47",
        "slug": "sqlalchemy",
        "title": "SQLAlchemy: ORM, сессии, связи",
        "description": "Разбираем SQLAlchemy: сессии, связи, конвертация.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQLAlchemy", "ORM", "SQL"],
        "learningOutcomes": ["Сессии", "Загрузка", "Модели"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции с объектами."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "47-p1", "title": "Коммит сессии", "difficulty": "easy", "slug": "session-commit"},
            {"taskId": "47-p2", "title": "Тип загрузки", "difficulty": "medium", "slug": "load-type"},
            {"taskId": "47-p3", "title": "Конвертация в dict", "difficulty": "hard", "slug": "model-dict"}
        ],
        "cheatSheet": {"summary60Sec": ["commit для сохранения", "lazy/joined загрузка", "obj.__dict__ для dict"]}
    },
    "problems": [
        {
            "id": "47-p1", "title": "Коммит сессии", "difficulty": "easy",
            "lecture_id": "47", "order": 1, "entry_function": "session_commit_behavior",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def session_commit_behavior(is_active: bool, has_changes: bool) -> bool:\n    ...",
            "description": "True, если сессия активна и есть изменения.",
            "examples": [{"input": "session_commit_behavior(True, True)", "output": "True"}],
            "args": [[True, True], [True, False]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "47-p2", "title": "Тип загрузки", "difficulty": "medium",
            "lecture_id": "47", "order": 2, "entry_function": "relationship_load_type",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def relationship_load_type(query_type: str) -> str:\n    ...",
            "description": "Вернуть 'joined' если eager, иначе 'lazy'.",
            "examples": [{"input": "relationship_load_type('eager')", "output": "'joined'"}],
            "args": [["eager"], ["lazy"]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "47-p3", "title": "Конвертация в dict", "difficulty": "hard",
            "lecture_id": "47", "order": 3, "entry_function": "model_to_dict",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def model_to_dict(obj) -> dict:\n    ...",
            "description": "Вернуть словарь полей (без начинающихся с _).",
            "examples": [{"input": "model_to_dict(obj)", "output": "{'a': 1}"}],
            "args": [[{'a': 1, '_b': 2}]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
