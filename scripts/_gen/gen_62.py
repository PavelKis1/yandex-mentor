"""Данные блока 62: Search."""
from genlib import run

LECTURE_SLUG = "62_search"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "62",
        "slug": "search",
        "title": "Search",
        "description": "Разбираем Search.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Search"],
        "learningOutcomes": ["Основы Search"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "62-p1", "title": "Задача 1", "difficulty": "easy", "slug": "t1"},
            {"taskId": "62-p2", "title": "Задача 2", "difficulty": "medium", "slug": "t2"},
            {"taskId": "62-p3", "title": "Задача 3", "difficulty": "hard", "slug": "t3"}
        ],
        "cheatSheet": {"summary60Sec": ["Функции для Search"]}
    },
    "problems": [
        {
            "id": "62-p1", "title": "Задача 1", "difficulty": "easy",
            "lecture_id": "62", "order": 1, "entry_function": "func_62_p1",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_62_p1() -> bool:\n    return True",
            "description": "Базовая задача.",
            "examples": [{"input": "func_62_p1()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "62-p2", "title": "Задача 2", "difficulty": "medium",
            "lecture_id": "62", "order": 2, "entry_function": "func_62_p2",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_62_p2() -> bool:\n    return True",
            "description": "Средняя задача.",
            "examples": [{"input": "func_62_p2()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "62-p3", "title": "Задача 3", "difficulty": "hard",
            "lecture_id": "62", "order": 3, "entry_function": "func_62_p3",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_62_p3() -> bool:\n    return True",
            "description": "Сложная задача.",
            "examples": [{"input": "func_62_p3()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
