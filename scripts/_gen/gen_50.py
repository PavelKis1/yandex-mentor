"""Данные блока 50: CI/CD."""
from genlib import run

LECTURE_SLUG = "50_cicd"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "50",
        "slug": "cicd",
        "title": "CI/CD",
        "description": "Разбираем CI/CD.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["CI/CD"],
        "learningOutcomes": ["Основы CI/CD"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "50-p1", "title": "Задача 1", "difficulty": "easy", "slug": "t1"},
            {"taskId": "50-p2", "title": "Задача 2", "difficulty": "medium", "slug": "t2"},
            {"taskId": "50-p3", "title": "Задача 3", "difficulty": "hard", "slug": "t3"}
        ],
        "cheatSheet": {"summary60Sec": ["Функции для CI/CD"]}
    },
    "problems": [
        {
            "id": "50-p1", "title": "Задача 1", "difficulty": "easy",
            "lecture_id": "50", "order": 1, "entry_function": "func_50_p1",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_50_p1() -> bool:\n    return True",
            "description": "Базовая задача.",
            "examples": [{"input": "func_50_p1()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "50-p2", "title": "Задача 2", "difficulty": "medium",
            "lecture_id": "50", "order": 2, "entry_function": "func_50_p2",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_50_p2() -> bool:\n    return True",
            "description": "Средняя задача.",
            "examples": [{"input": "func_50_p2()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "50-p3", "title": "Задача 3", "difficulty": "hard",
            "lecture_id": "50", "order": 3, "entry_function": "func_50_p3",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_50_p3() -> bool:\n    return True",
            "description": "Сложная задача.",
            "examples": [{"input": "func_50_p3()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
