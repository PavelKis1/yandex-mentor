"""Данные блока 31: Optimization (улучшение сложности)."""
from genlib import run

LECTURE_SLUG = "31_optimization"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "31",
        "slug": "optimization",
        "title": "Optimization: два указателя, хеш-таблицы, бинарный поиск",
        "description": "Ускоряем алгоритмы: пары через два указателя за O(n), дубликаты через set-«уже видели», поиск за O(log n) без bisect.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Optimization", "Two Pointers", "Binary Search"],
        "learningOutcomes": [
            "Использовать два указателя для отсортированных данных",
            "Применять set для проверки «уже видели» за O(1)",
            "Реализовать бинарный поиск без встроенного bisect"
        ],
        "complexity": {
            "timeComplexity": "O(n) и O(log n) на задачи блока",
            "spaceComplexity": "O(1)–O(n)",
            "explanation": "Главная цель — снизить сложность с O(n²) до O(n) или O(log n)."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Когда два указателя работают за O(n)?",
                "options": [
                    {"id": "opt1", "text": "Когда массив отсортирован и монотонно двигаем края", "isCorrect": True, "explanation": "Каждый шаг двигает один из указателей, суммарно O(n)."},
                    {"id": "opt2", "text": "Всегда, независимо от данных", "isCorrect": False, "explanation": "Требуется отсортированность для однозначного выбора."},
                    {"id": "opt3", "text": "Только когда есть дубликаты", "isCorrect": False, "explanation": "Дубликаты не обязательны."}
                ],
                "hint": "Почему указатель не ходит назад?"
            },
            {
                "id": "q2",
                "question": "Почему set-проверка «уже видели» даёт O(1)?",
                "options": [
                    {"id": "opt1", "text": "Хеш-таблица в среднем за O(1)", "isCorrect": True, "explanation": "Поиск по хешу даёт константное время в среднем."},
                    {"id": "opt2", "text": "Set хранит элементы отсортированно", "isCorrect": False, "explanation": "Set не сортирует."},
                    {"id": "opt3", "text": "Set никогда не растёт", "isCorrect": False, "explanation": "Set растёт, но амортизированно O(1)."}
                ],
                "hint": "Какая структура даёт быстрый поиск?"
            }
        ],
        "attachedTasks": [
            {"taskId": "31-p1", "title": "Два указателя: пара по сумме", "difficulty": "easy", "slug": "two-pointers"},
            {"taskId": "31-p2", "title": "Первый дубликат через set", "difficulty": "medium", "slug": "first-duplicate-index"},
            {"taskId": "31-p3", "title": "Бинарный поиск без bisect", "difficulty": "hard", "slug": "binary-search"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Два указателя: сходите к центру, выбирая шаг по сумме.",
                "set «уже видели» превращает O(n²) в O(n).",
                "Бинарный поиск каждый шаг делит диапазон пополам — O(log n)."
            ]
        }
    },
    "problems": [
        {
            "id": "31-p1", "title": "Два указателя: пара по сумме", "difficulty": "easy",
            "lecture_id": "31", "order": 1, "entry_function": "two_pointers",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def two_pointers(nums: list[int], target: int) -> list[int] | None:\n    \"\"\"Пару (x, y) из отсортированного nums с суммой target; None, если нет.\"\"\"\n    ...",
            "description": "Дан **отсортированный по возрастанию** список `nums`. Найдите любую пару `(x, y)` (два разных элемента), сумма которых равна `target`, за `O(n)` через **два указателя**. Верните её как список `[x, y]` или `None`, если пары нет.\n\n**Функция решения:**\n\n```python\ndef two_pointers(nums: list[int], target: int) -> list[int] | None:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,2,3,4,6], target = 8", "output": "[2,6]", "explanation": "2+6=8."},
                {"input": "nums = [1,2,3], target = 99", "output": "None", "explanation": "Подходящей пары нет."}
            ],
            "constraints": ["2 ≤ len(nums) ≤ 10^5; nums отсортирован"],
            "hints": [
                "left=0, right=len(nums)-1; сравнивайте sum.",
                "Если sum < target — двигайте left вправо, иначе right влево."
            ],
            "args": [
                [[1, 2, 3, 4, 6], 8],
                [[1, 2, 3], 99],
                [[1, 3, 5, 7], 8],
                [[-2, 0, 2, 4], 2],
                [[1, 2], 3],
                [[5, 5, 5, 5, 5], 10]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "31-p2", "title": "Первый дубликат через set", "difficulty": "medium",
            "lecture_id": "31", "order": 2, "entry_function": "first_duplicate_index",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def first_duplicate_index(nums: list[int]) -> int:\n    \"\"\"Индекс первого повторно встреченного элемента (set «уже видели»); -1, если нет.\"\"\"\n    ...",
            "description": "Дан список `nums`. Найдите **индекс первого элемента, который уже встречался ранее** (второе вхождение какого-то числа). Используйте `set` для проверки «уже видели» за `O(1)` — это заменяет вложенный цикл `O(n²)` на `O(n)`. Если дубликатов нет, верните `-1`.\n\n**Функция решения:**\n\n```python\ndef first_duplicate_index(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [2,1,3,2,4]", "output": "3", "explanation": "2 встречается на индексах 0 и 3 — первое повторное вхождение на 3."},
                {"input": "nums = [1,2,3]", "output": "-1", "explanation": "Повторов нет."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 10^5"],
            "hints": [
                "Держите set виденных значений.",
                "Если текущее уже в set — верните его индекс."
            ],
            "args": [
                [[2, 1, 3, 2, 4]],
                [[1, 2, 3]],
                [[0, 0]],
                [[1, 2, 3, 1]],
                [[7]],
                [[1, 2, 1, 2]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "31-p3", "title": "Бинарный поиск без bisect", "difficulty": "hard",
            "lecture_id": "31", "order": 3, "entry_function": "binary_search",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def binary_search(nums: list[int], target: int) -> int:\n    \"\"\"Индекс target в отсортированном nums за O(log n); -1, если нет (без bisect).\"\"\"\n    ...",
            "description": "Дан **отсортированный** список `nums` и `target`. Верните **индекс** `target` за `O(log n)`, реализовав **бинарный поиск вручную** (без `bisect`). Если элемента нет — верните `-1`.\n\n**Функция решения:**\n\n```python\ndef binary_search(nums: list[int], target: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,3,5,7,9], target = 5", "output": "2", "explanation": "5 стоит на индексе 2."},
                {"input": "nums = [1,3,5,7,9], target = 2", "output": "-1", "explanation": "Двойки нет."}
            ],
            "constraints": ["nums отсортирован по возрастанию; 0 ≤ len ≤ 10^6"],
            "hints": [
                "mid = (l + r) // 2, сужайте диапазон вдвое.",
                "При nums[mid] < target — ищите в правой половине."
            ],
            "args": [
                [[1, 3, 5, 7, 9], 5],
                [[1, 3, 5, 7, 9], 2],
                [[], 5],
                [[3], 3],
                [[1, 2, 2, 3], 2],
                [[10, 20, 30], 30]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])