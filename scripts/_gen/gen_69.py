"""Данные блока 69: Mocks4."""
from genlib import run

LECTURE_SLUG = "69_mocks4"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "69",
        "slug": "mocks4",
        "title": "Mocks4",
        "description": "Разбираем Mocks4.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Mocks4"],
        "learningOutcomes": ["Основы Mocks4"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "69-p1", "title": "Задача 1", "difficulty": "easy", "slug": "t1"},
            {"taskId": "69-p2", "title": "Задача 2", "difficulty": "medium", "slug": "t2"},
            {"taskId": "69-p3", "title": "Задача 3", "difficulty": "hard", "slug": "t3"}
        ],
        "cheatSheet": {"summary60Sec": ["Функции для Mocks4"]}
    },
    "problems": [
        {
            "id": "69-p1", "title": "Задача 1", "difficulty": "easy",
            "lecture_id": "69", "order": 1, "entry_function": "func_69_p1",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_69_p1() -> bool:\n    return True",
            "description": "Базовая задача.",
            "examples": [{"input": "func_69_p1()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "69-p2", "title": "Задача 2", "difficulty": "medium",
            "lecture_id": "69", "order": 2, "entry_function": "func_69_p2",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_69_p2() -> bool:\n    return True",
            "description": "Средняя задача.",
            "examples": [{"input": "func_69_p2()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "69-p3", "title": "Задача 3", "difficulty": "hard",
            "lecture_id": "69", "order": 3, "entry_function": "func_69_p3",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def func_69_p3() -> bool:\n    return True",
            "description": "Сложная задача.",
            "examples": [{"input": "func_69_p3()", "output": "True"}],
            "args": [[]],
            "hidden": [True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
