"""Данные блока 68: Mocks3."""
from genlib import run

LECTURE_SLUG = "68_mocks3"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "68",
        "slug": "mocks3",
        "title": "Mocks3",
        "description": "Разбираем Mocks3.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Mocks3"],
        "learningOutcomes": ["Основы Mocks3"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "68-p1", "title": "Задача 1", "difficulty": "easy", "slug": "t1"},
            {"taskId": "68-p2", "title": "Задача 2", "difficulty": "medium", "slug": "t2"},
            {"taskId": "68-p3", "title": "Задача 3", "difficulty": "hard", "slug": "t3"}
        ],
        "cheatSheet": {"summary60Sec": ["Функции для Mocks3"]}
    },
    "problems": [
        {
            "id": "68-p1", "title": "Задача 1", "difficulty": "easy",
            "lecture_id": "68", "order": 1, "entry_function": "func_68_p1",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_68_p1() -> bool:\n    return True",
            "description": "Базовая задача.",
            "examples": [{"input": "func_68_p1()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "68-p2", "title": "Задача 2", "difficulty": "medium",
            "lecture_id": "68", "order": 2, "entry_function": "func_68_p2",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_68_p2() -> bool:\n    return True",
            "description": "Средняя задача.",
            "examples": [{"input": "func_68_p2()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "68-p3", "title": "Задача 3", "difficulty": "hard",
            "lecture_id": "68", "order": 3, "entry_function": "func_68_p3",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_68_p3() -> bool:\n    return True",
            "description": "Сложная задача.",
            "examples": [{"input": "func_68_p3()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
