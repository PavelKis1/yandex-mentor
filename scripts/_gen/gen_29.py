"""Данные блока 29: Python Internals (внутренности Python)."""
from genlib import run

LECTURE_SLUG = "29_python_internals"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "29",
        "slug": "python-internals",
        "title": "Python Internals: ссылки, замыкания, генераторы",
        "description": "Как Python работает под капотом: мутабельность и передача по ссылке, замыкания с nonlocal, ленивые генераторы через yield. Разбираем через выполнимые задачи на счётчики и простые числа.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Internals", "Closures", "Generators"],
        "learningOutcomes": [
            "Понимать мутабельность списков и передачу по ссылке",
            "Строить замыкания с nonlocal и фабрики функций",
            "Использовать генераторы и понимать ленивость"
        ],
        "complexity": {
            "timeComplexity": "Варьируется: O(1) на шаг генератора",
            "spaceComplexity": "Генераторы хранят только состояние (O(1))",
            "explanation": "Замыкание хранит окружение O(1); генератор вычисляет значения лениво, не строя весь список."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что меняет nonlocal внутри замыкания?",
                "options": [
                    {"id": "opt1", "text": "Переменную из объемлющей функции", "isCorrect": True, "explanation": "nonlocal связывает имя с переменной внешнего scope."},
                    {"id": "opt2", "text": "Глобальную переменную", "isCorrect": False, "explanation": "Для глобальных нужен global."},
                    {"id": "opt3", "text": "Создаёт новую локальную переменную", "isCorrect": False, "explanation": "Без nonlocal присваивание создаёт новую локальную."}
                ],
                "hint": "Какое ключевое слово сохраняет состояние между вызовами?"
            },
            {
                "id": "q2",
                "question": "Почему генератор с yield экономит память?",
                "options": [
                    {"id": "opt1", "text": "Значения вычисляются по одному за раз", "isCorrect": True, "explanation": "Генератор хранит только текущее состояние, не весь список."},
                    {"id": "opt2", "text": "Он хранит все значения в кэше", "isCorrect": False, "explanation": "Это противоречит ленивости."},
                    {"id": "opt3", "text": "Он использует компрессию", "isCorrect": False, "explanation": "Никакой компрессии нет."}
                ],
                "hint": "Что делает yield — возвращает всё сразу или по одному?"
            }
        ],
        "attachedTasks": [
            {"taskId": "29-p1", "title": "Списки: мутабельность", "difficulty": "easy", "slug": "append-unique"},
            {"taskId": "29-p2", "title": "Замыкание-счётчик", "difficulty": "medium", "slug": "closure-counter"},
            {"taskId": "29-p3", "title": "Генератор простых чисел", "difficulty": "hard", "slug": "first-primes"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Списки мутабельны и передаются по ссылке — изменение внутри функции видно снаружи.",
                "Замыкание: внутренняя функция запоминает окружение; nonlocal меняет переменную внешней.",
                "Генератор с yield вычисляет значения лениво, экономя память.",
                "GIL ограничивает одновременное исполнение Python-кода одним потоком.",
                "lru_cache и замыкания — способы держать состояние между вызовами."
            ]
        }
    },
    "problems": [
        {
            "id": "29-p1", "title": "Списки: мутабельность", "difficulty": "easy",
            "lecture_id": "29", "order": 1, "entry_function": "append_unique",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def append_unique(lst: list[int], value: int) -> bool:\n    \"\"\"Добавить value в lst (in-place), если его ещё нет, и вернуть True; иначе — False.\"\"\"\n    ...",
            "description": "Вспомните, что списки **мутабельны** и передаются по ссылке. Реализуйте функцию, которая добавляет `value` в список `lst` **in-place**, если такого элемента ещё нет (и возвращает `True`), либо ничего не меняет и возвращает `False`.\n\n**Функция решения:**\n\n```python\ndef append_unique(lst: list[int], value: int) -> bool:\n    ...\n```",
            "examples": [
                {"input": "lst = [1,2], value = 3", "output": "True", "explanation": "3 ещё нет — добавляем, список меняется in-place."},
                {"input": "lst = [1,2], value = 2", "output": "False", "explanation": "2 уже есть — не добавляем."}
            ],
            "constraints": ["1 ≤ len(lst) ≤ 10^5"],
            "hints": [
                "Проверьте value not in lst и вызовите lst.append(value).",
                "Мутация in-place означает, что вызывающий увидит изменения в списке."
            ],
            "args": [
                [[1, 2], 3],
                [[1, 2], 2],
                [[], 0],
                [[5, 5], 5],
                [[1, 2, 3], 4],
                [[0], 1],
                [[7, 8, 9], 9]
            ],
            "hidden": [False, False, True, True, False, True, True]
        },
        {
            "id": "29-p2", "title": "Замыкание-счётчик", "difficulty": "medium",
            "lecture_id": "29", "order": 2, "entry_function": "closure_counter",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def closure_counter(steps: int) -> list[int]:\n    \"\"\"Вернуть 1..steps, вычисленные счётчиком-замыканием через nonlocal.\"\"\"\n    ...",
            "description": "Реализуйте **счётчик-замыкание**: внешняя функция создаёт локальную неотрицательную переменную и возвращает внутреннюю функцию, которая через `nonlocal` увеличивает счётчик и возвращает очередное значение. Вызовите счётчик `steps` раз и верните список `1..steps`.\n\n**Функция решения:**\n\n```python\ndef closure_counter(steps: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "steps = 3", "output": "[1,2,3]", "explanation": "Каждый вызов внутренней функции возвращает следующее значение счётчика."}
            ],
            "constraints": ["0 ≤ steps ≤ 1000"],
            "hints": [
                "Внутренняя функция объявляет nonlocal count и делает count += 1.",
                "Накопите результаты в список, вызывая внутреннюю функцию steps раз."
            ],
            "args": [
                [3],
                [1],
                [5],
                [0],
                [2],
                [10]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "29-p3", "title": "Генератор простых чисел", "difficulty": "hard",
            "lecture_id": "29", "order": 3, "entry_function": "first_primes",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def first_primes(n: int) -> list[int]:\n    \"\"\"Вернуть первые n простых чисел (минимум через генератор с yield).\"\"\"\n    ...",
            "description": "Напишите **генератор** (функцию с `yield`), который лениво выдаёт простые числа по возрастанию. Верните **первые `n`** простых чисел списком. Значения должны вычисляться по одному, а не строиться заранее.\n\n**Функция решения:**\n\n```python\ndef first_primes(n: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "n = 3", "output": "[2,3,5]", "explanation": "Первые три простых числа."},
                {"input": "n = 1", "output": "[2]", "explanation": "Минимальное простое — 2."}
            ],
            "constraints": ["0 ≤ n ≤ 1000"],
            "hints": [
                "Генератор: def gen(): ... yield p — вычисляет p по одному за раз.",
                "Проверяйте делители до корня из числа; возьмите n значений из генератора."
            ],
            "args": [
                [3],
                [1],
                [5],
                [10],
                [0],
                [4],
                [7]
            ],
            "hidden": [False, False, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])