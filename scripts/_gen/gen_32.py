"""Данные блока 32: Decorators (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "32_decorators"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "32",
        "slug": "decorators",
        "title": "Decorators: таймер, логирование, повтор с задержкой",
        "description": "Декораторы меняют поведение функций. Проверяем их по детерминированному результату: что время/логи/повторы не ломают возвращаемое значение.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Decorators", "functools"],
        "learningOutcomes": [
            "Сохранять имя функции через functools.wraps",
            "Писать логирующий декоратор с *args/**kwargs",
            "Повторять вызовы при исключении через декоратор-параметр"
        ],
        "complexity": {
            "timeComplexity": "O(1) на обёртку",
            "spaceComplexity": "O(1) дополнительно",
            "explanation": "Декораторы добавляют константный оверхед поверх вызываемой функции."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Зачем нужен functools.wraps в декораторе?",
                "options": [
                    {"id": "opt1", "text": "Сохраняет __name__ и __doc__ исходной функции", "isCorrect": True, "explanation": "Wraps копирует метаданные, помогая отладке."},
                    {"id": "opt2", "text": "Ускоряет вызовы", "isCorrect": False, "explanation": "Оверхед не снижает."},
                    {"id": "opt3", "text": "Запрещает изменение функции", "isCorrect": False, "explanation": "К тому же не про запрет."}
                ],
                "hint": "Что теряется без wraps?"
            },
            {
                "id": "q2",
                "question": "Что вернёт @timed для результата функции?",
                "options": [
                    {"id": "opt1", "text": "Тот же результат, что и функция", "isCorrect": True, "explanation": "Декоратор-таймер лишь замеряет время и возвращает результат исходной функции."},
                    {"id": "opt2", "text": "Время выполнения", "isCorrect": False, "explanation": "Время печатается, но возвращается исходный результат."},
                    {"id": "opt3", "text": "None", "isCorrect": False, "explanation": "Декоратор должен пробросить результат."}
                ],
                "hint": "Что делает обёрнутая функция?"
            }
        ],
        "attachedTasks": [
            {"taskId": "32-p1", "title": "Таймер-декоратор", "difficulty": "easy", "slug": "timed-sum"},
            {"taskId": "32-p2", "title": "Логирование вызовов", "difficulty": "medium", "slug": "logged-add"},
            {"taskId": "32-p3", "title": "Повтор с задержкой", "difficulty": "hard", "slug": "retry-success"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Декоратор = функция, принимающая функцию и возвращающая обёртку.",
                "functools.wraps сохраняет метаданные исходной функции.",
                "Таймер печатает время, но возвращает исходный результат.",
                "retry повторяет вызов и пробрасывает ошибку после последней попытки."
            ]
        }
    },
    "problems": [
        {
            "id": "32-p1", "title": "Таймер-декоратор", "difficulty": "easy",
            "lecture_id": "32", "order": 1, "entry_function": "timed_sum",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "import functools, time\n\ndef timed(fn):\n    \"\"\"Декоратор, печатает время и возвращает результат функции без изменений.\"\"\"\n    ...\n\ndef timed_sum(nums: list[int]) -> int:\n    \"\"\"Вернуть сумму nums, применив @timed к внутренней функции.\"\"\"\n    ...",
            "description": "Напишите декоратор `@timed`, который печатает время выполнения функции в миллисекундах и **возвращает результат без изменений**. Затем реализуйте `timed_sum(nums)`, которая применяет `@timed` к функции суммирования и возвращает её результат (`sum(nums)`). Проверяется именно результат — таймер не должен его ломать.\n\n**Функция решения:**\n\n```python\ndef timed_sum(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,2,3]", "output": "6", "explanation": "Сумма при сохранении результата декоратором."},
                {"input": "nums = []", "output": "0", "explanation": "Сумма пустого списка — 0."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 10^5"],
            "hints": [
                "functools.wraps(f) сохраняет __name__.",
                "time.perf_counter() до и после вызова; верните res как есть."
            ],
            "args": [
                [[1, 2, 3]],
                [[]],
                [[5]],
                [[-1, 10, -3, 7]],
                [[0, 0, 0]],
                [[2, 4, 6, 8]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "32-p2", "title": "Логирование вызовов", "difficulty": "medium",
            "lecture_id": "32", "order": 2, "entry_function": "logged_add",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "LOG: list = []\n\ndef logger(fn):\n    \"\"\"Декоратор, логирует имя, аргументы и результат в LOG.\"\"\"\n    ...\n\ndef logged_add(a: int, b: int):\n    \"\"\"Вернуть список [a+b, число записей в LOG после вызова @logger].\"\"\"\n    ...",
            "description": "Напишите декоратор `@logger`, который при каждом вызове дописывает в список `LOG` кортеж `(имя_функции, args, результат)`. Реализуйте `logged_add(a, b)`, которая применяет `@logger` к сложению `a` и `b` и возвращает **список** `[a + b, len(LOG)]` после одного вызова.\n\n**Функция решения:**\n\n```python\ndef logged_add(a: int, b: int):\n    ...\n```",
            "examples": [
                {"input": "logged_add(1, 2)", "output": "[3, 1]", "explanation": "Результат 3 и ровно одна запись в LOG."}
            ],
            "constraints": ["Целые числа |a|,|b| ≤ 10^6"],
            "hints": [
                "Обёртка принимает *args, **kwargs и возвращает результат.",
                "LOG.append((fn.__name__, args, result)); верните (result, len(LOG))."
            ],
            "args": [
                [1, 2],
                [5, 7],
                [-3, 3],
                [0, 0],
                [10, 20],
                [100, 200]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "32-p3", "title": "Повтор с задержкой", "difficulty": "hard",
            "lecture_id": "32", "order": 3, "entry_function": "retry_success",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "import time\n\ndef retry(times=3, delay=0.1):\n    \"\"\"Декоратор-параметр: повторяет вызов при исключении, после times попыток пробрасывает.\"\"\"\n    ...\n\ndef retry_success(failures: int) -> int:\n    \"\"\"Сколько попыток сделает @retry(times=3), если функция падает первые `failures` раз.\"\"\"\n    ...",
            "description": "Напишите декоратор `@retry(times=3, delay=0.1)`, который при исключении повторяет вызов и пробрасывает ошибку после `times` неудачных попыток. Функция-внутренность падает первые `failures` вызовов (для `failures < times`) и на следующем вызывает успех. Верните **число сделанных попыток**.\n\n**Функция решения:**\n\n```python\ndef retry_success(failures: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "failures = 1", "output": "2", "explanation": "1-я попытка упала, 2-я успешна — потребовалось 2 попытки."},
                {"input": "failures = 0", "output": "1", "explanation": "Успех с первой попытки."}
            ],
            "constraints": ["0 ≤ failures ≤ 2 (times=3)"],
            "hints": [
                "for i in range(times): try: return f(*a,**kw) except: time.sleep(delay) — после цикла пробросить.",
                "Считайте попытки счётчиком; верните счётчик на момент успеха."
            ],
            "args": [
                [0],
                [1],
                [2],
                [0],
                [1],
                [2]
            ],
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])