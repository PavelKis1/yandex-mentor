"""Данные блока 46: FastAPI."""
from genlib import run

LECTURE_SLUG = "46_fastapi"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "46",
        "slug": "fastapi",
        "title": "FastAPI: маршрутизация, модели, зависимости",
        "description": "Разбираем FastAPI: маршруты, Pydantic, DI.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["FastAPI", "Python", "API"],
        "learningOutcomes": ["Маршруты", "Валидация", "DI"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции с API."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "46-p1", "title": "Сопоставление маршрутов", "difficulty": "easy", "slug": "route-match"},
            {"taskId": "46-p2", "title": "Валидация Pydantic", "difficulty": "medium", "slug": "pydantic-model"},
            {"taskId": "46-p3", "title": "Зависимости", "difficulty": "hard", "slug": "di-order"}
        ],
        "cheatSheet": {"summary60Sec": ["Маршруты с {}", "Pydantic для схем", "Depends для DI"]}
    },
    "problems": [
        {
            "id": "46-p1", "title": "Сопоставление маршрутов", "difficulty": "easy",
            "lecture_id": "46", "order": 1, "entry_function": "fastapi_route_match",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def fastapi_route_match(route: str, path: str) -> bool:\n    ...",
            "description": "True, если path совпадает с route (например, /users/{id} совпадает с /users/1).",
            "examples": [{"input": "fastapi_route_match('/users/{id}', '/users/1')", "output": "True"}],
            "args": [["/users/{id}", "/users/1"], ["/users", "/users"]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "46-p2", "title": "Валидация Pydantic", "difficulty": "medium",
            "lecture_id": "46", "order": 2, "entry_function": "validate_pydantic_model",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def validate_pydantic_model(data: dict, schema: dict) -> bool:\n    ...",
            "description": "True, если data соответствует типам в schema.",
            "examples": [{"input": "validate_pydantic_model({'id': 1}, {'id': 'int'})", "output": "True"}],
            "args": [[{'id': 1}, {'id': 'int'}], [{'id': '1'}, {'id': 'int'}]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "46-p3", "title": "Зависимости", "difficulty": "hard",
            "lecture_id": "46", "order": 3, "entry_function": "dependency_injection_order",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def dependency_injection_order(dependencies: list) -> list:\n    ...",
            "description": "Вернуть список зависимостей в порядке разрешения (по весу).",
            "examples": [{"input": "dependency_injection_order([('a', 2), ('b', 1)])", "output": "['b', 'a']"}],
            "args": [[[('a', 2), ('b', 1)]]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
