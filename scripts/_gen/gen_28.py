"""Данные блока 28: Functools (инструменты высшего порядка)."""
from genlib import run

LECTURE_SLUG = "28_functools"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "28",
        "slug": "functools",
        "title": "Functools: partial, lru_cache, reduce",
        "description": "Модуль functools — для функций высшего порядка: lru_cache кеширует вычисления, partial фиксирует аргументы, reduce сводит последовательность. Разбираем практику на ценах, Фибоначчи и поиске максимума.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Standard Library", "Functional Programming"],
        "learningOutcomes": [
            "Использовать lru_cache для мемоизации рекурсии",
            "Фиксировать аргументы функций через partial",
            "Сводить последовательность через reduce"
        ],
        "complexity": {
            "timeComplexity": "lru_cache: O(n), reduce: O(n)",
            "spaceComplexity": "lru_cache: O(n), partial: O(1)",
            "explanation": "lru_cache превращает экспоненциальную рекурсию в линейную, храня ранее вычисленные значения."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что делает functools.lru_cache?",
                "options": [
                    {"id": "opt1", "text": "Кеширует результаты функции по аргументам", "isCorrect": True, "explanation": "Повторные вызовы с теми же аргументами берутся из кэша."},
                    {"id": "opt2", "text": "Сортирует аргументы", "isCorrect": False, "explanation": "К кэшу отношения не имеет."},
                    {"id": "opt3", "text": "Делает функцию потокобезопасной", "isCorrect": False, "explanation": "Не про потоки."}
                ],
                "hint": "Как ускоряется повторяющаяся рекурсия?"
            },
            {
                "id": "q2",
                "question": "Зачем нужен functools.partial?",
                "options": [
                    {"id": "opt1", "text": "Зафиксировать часть аргументов функции", "isCorrect": True, "explanation": "partial создаёт новую функцию с предзаданными аргументами."},
                    {"id": "opt2", "text": "Частично выполнить функцию", "isCorrect": False, "explanation": "Функция не выполняется до вызова."},
                    {"id": "opt3", "text": "Импортировать модуль частично", "isCorrect": False, "explanation": "Не про импорт."}
                ],
                "hint": "Что «частичного» в partial?"
            }
        ],
        "attachedTasks": [
            {"taskId": "28-p1", "title": "Цены со скидкой", "difficulty": "easy", "slug": "partial-discount"},
            {"taskId": "28-p2", "title": "Мемоизация", "difficulty": "medium", "slug": "memoized-fib"},
            {"taskId": "28-p3", "title": "Редукция", "difficulty": "hard", "slug": "reduce-max"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "@lru_cache(maxsize=None) на внутренней функции убирает повторные вычисления.",
                "partial(fn, rate=0.1) фиксирует аргумент и возвращает новую функцию.",
                "reduce(lambda a,b: a if a>b else b, nums) — свёртка слева направо.",
                "wraps сохраняет имя и docstring при написании декораторов.",
                "Мемоизация меняет экспоненциальную сложность на линейную."
            ]
        }
    },
    "problems": [
        {
            "id": "28-p1", "title": "Цены со скидкой", "difficulty": "easy",
            "lecture_id": "28", "order": 1, "entry_function": "discounted_prices",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def discounted_prices(prices: list[int], percent: int) -> list[int]:\n    \"\"\"Вернуть цены после скидки percent (целые, округление вниз).\"\"\"\n    ...",
            "description": "Даны цены `prices` и скидка `percent` (0–100). Через `functools.partial` зафиксируйте ставку и примените функцию ко всем ценам. Верните список цен после скидки (целые числа, деление с округлением вниз).\n\n**Функция решения:**\n\n```python\ndef discounted_prices(prices: list[int], percent: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "prices = [100,200,300], percent = 10", "output": "[90,180,270]", "explanation": "Цена после скидки 10% = price * 90 // 100."}
            ],
            "constraints": ["1 ≤ len(prices) ≤ 10^4", "0 ≤ percent ≤ 100"],
            "hints": [
                "Внутренняя функция берёт price, partial фиксирует percent.",
                "Итог: int(price * (100 - percent) // 100)."
            ],
            "args": [
                [[100, 200, 300], 10],
                [[100, 200], 25],
                [[10, 20, 30], 20],
                [[50, 50], 0],
                [[1, 2, 3], 100],
                [[400, 500], 50],
                [[7], 30]
            ],
            "hidden": [False, True, False, True, True, True, True]
        },
        {
            "id": "28-p2", "title": "Мемоизация", "difficulty": "medium",
            "lecture_id": "28", "order": 2, "entry_function": "fib",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def fib(n: int) -> int:\n    \"\"\"n-е число Фибоначчи с кэшированием через functools.lru_cache.\"\"\"\n    ...",
            "description": "Реализуйте рекурсивную функцию `fib(n)`, возвращающую **n-е** число Фибоначчи, с кэшированием через `functools.lru_cache`. Должно работать быстро даже для больших `n`.\n\n**Функция решения:**\n\n```python\ndef fib(n: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "n = 10", "output": "55", "explanation": "Ряд: 0,1,1,2,3,5,8,13,21,34,55."}
            ],
            "constraints": ["0 ≤ n ≤ 1000"],
            "hints": [
                "Поместите @lru_cache(maxsize=None) на внутреннюю рекурсивную функцию.",
                "База: fib(0)=0, fib(1)=1."
            ],
            "args": [
                [0],
                [1],
                [10],
                [20],
                [5],
                [50],
                [100]
            ],
            "hidden": [False, False, True, True, False, True, True]
        },
        {
            "id": "28-p3", "title": "Редукция", "difficulty": "hard",
            "lecture_id": "28", "order": 3, "entry_function": "reduce_max",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def reduce_max(nums: list[int]) -> int:\n    \"\"\"Максимум списка через functools.reduce (без встроенного max).\"\"\"\n    ...",
            "description": "Дан список чисел `nums`. Найдите **максимальный элемент** через `functools.reduce`, не используя встроенный `max()`. Для пустого списка верните `None`.\n\n**Функция решения:**\n\n```python\ndef reduce_max(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [3,7,2,9,5]", "output": "9", "explanation": "Свёртка с сохранением большего из двух."},
                {"input": "nums = []", "output": "None", "explanation": "Максимум пустого списка не определён."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 10^5"],
            "hints": [
                "reduce(lambda a,b: a if a > b else b, nums).",
                "При пустом списке верните None до вызова reduce."
            ],
            "args": [
                [[3, 7, 2, 9, 5]],
                [[]],
                [[5]],
                [[1, 1, 1, 1]],
                [[-3, -1, -7]],
                [[0, -5, 10, 2]],
                [[100, 50, 75]]
            ],
            "hidden": [False, False, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])