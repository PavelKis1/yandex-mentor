"""Данные блока 45: REST API."""
from genlib import run

LECTURE_SLUG = "45_rest"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "45",
        "slug": "rest",
        "title": "REST API: ресурсы, методы, форматы",
        "description": "Разбираем принципы REST: ресурсы, HTTP-методы, query-параметры.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["REST", "API", "HTTP"],
        "learningOutcomes": ["Парсить параметры", "Выбирать метод", "Валидировать URI"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции с URI."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "45-p1", "title": "Парсинг параметров", "difficulty": "easy", "slug": "parse-params"},
            {"taskId": "45-p2", "title": "Выбор REST метода", "difficulty": "medium", "slug": "rest-method"},
            {"taskId": "45-p3", "title": "Валидация URI", "difficulty": "hard", "slug": "valid-uri"}
        ],
        "cheatSheet": {"summary60Sec": ["GET - чтение", "POST - создание", "PUT - обновление", "DELETE - удаление"]}
    },
    "problems": [
        {
            "id": "45-p1", "title": "Парсинг параметров", "difficulty": "easy",
            "lecture_id": "45", "order": 1, "entry_function": "parse_url_params",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def parse_url_params(url: str) -> dict:\n    \"\"\"Вернуть словарь query-параметров из URL.\"\"\"\n    ...",
            "description": "Верните словарь query-параметров из URL.",
            "examples": [{"input": "parse_url_params('a.com?x=1')", "output": "{'x': '1'}"}],
            "args": [["a.com?x=1"], ["b.com?y=2&z=3"]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "45-p2", "title": "Выбор REST метода", "difficulty": "medium",
            "lecture_id": "45", "order": 2, "entry_function": "rest_method_for",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def rest_method_for(action: str) -> str:\n    \"\"\"Вернуть HTTP-метод для действия (create, read, update, delete).\"\"\"\n    ...",
            "description": "Вернуть HTTP-метод: create->POST, read->GET, update->PUT, delete->DELETE.",
            "examples": [{"input": "rest_method_for('create')", "output": "'POST'"}],
            "args": [["create"], ["read"], ["update"], ["delete"]],
            "hidden": [False, False, False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "45-p3", "title": "Валидация URI", "difficulty": "hard",
            "lecture_id": "45", "order": 3, "entry_function": "is_valid_rest_uri",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def is_valid_rest_uri(uri: str) -> bool:\n    \"\"\"True, если URI соответствует REST (/resource или /resource/id).\"\"\"\n    ...",
            "description": "True, если URI соответствует `/resource` или `/resource/id`.",
            "examples": [{"input": "is_valid_rest_uri('/users')", "output": "True"}],
            "args": [["/users"], ["/users/1"], ["/users/1/posts"], ["invalid"]],
            "hidden": [False, False, False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
