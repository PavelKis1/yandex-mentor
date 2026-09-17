"""Данные блока 54: Network."""
from genlib import run

LECTURE_SLUG = "54_network"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "54",
        "slug": "network",
        "title": "Network",
        "description": "Разбираем Network.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Network"],
        "learningOutcomes": ["Основы Network"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "54-p1", "title": "Задача 1", "difficulty": "easy", "slug": "t1"},
            {"taskId": "54-p2", "title": "Задача 2", "difficulty": "medium", "slug": "t2"},
            {"taskId": "54-p3", "title": "Задача 3", "difficulty": "hard", "slug": "t3"}
        ],
        "cheatSheet": {"summary60Sec": ["Функции для Network"]}
    },
    "problems": [
        {
            "id": "54-p1", "title": "Задача 1", "difficulty": "easy",
            "lecture_id": "54", "order": 1, "entry_function": "func_54_p1",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_54_p1() -> bool:\n    return True",
            "description": "Базовая задача.",
            "examples": [{"input": "func_54_p1()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "54-p2", "title": "Задача 2", "difficulty": "medium",
            "lecture_id": "54", "order": 2, "entry_function": "func_54_p2",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_54_p2() -> bool:\n    return True",
            "description": "Средняя задача.",
            "examples": [{"input": "func_54_p2()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "54-p3", "title": "Задача 3", "difficulty": "hard",
            "lecture_id": "54", "order": 3, "entry_function": "func_54_p3",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_54_p3() -> bool:\n    return True",
            "description": "Сложная задача.",
            "examples": [{"input": "func_54_p3()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
