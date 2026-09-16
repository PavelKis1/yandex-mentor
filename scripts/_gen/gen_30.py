"""Данные блока 30: Profiling & Performance (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "30_profiling"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "30",
        "slug": "profiling",
        "title": "Profiling & Performance: замеры, узкие места, память",
        "description": "Учимся находить узкие места: почему comprehension быстрее append-цикла, где тратится память и время. Задачи детерминированы — проверяем результат, а не миллисекунды.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Profiling", "Performance", "Perf"],
        "learningOutcomes": [
            "Строить списки через list comprehension",
            "Находить дубликаты за O(n) через set",
            "Оценивать память и время алгоритма"
        ],
        "complexity": {
            "timeComplexity": "O(n) на задачи блока",
            "spaceComplexity": "O(1)–O(n) в зависимости от задачи",
            "explanation": "Замер времени vbenchmark не стабилен, поэтому задачи проверяются по детерминированному результату, а не по миллисекундам."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Почему list comprehension обычно быстрее for с append?",
                "options": [
                    {"id": "opt1", "text": "Меньше байткод-инструкций и нет лишних вызовов метода", "isCorrect": True, "explanation": "Comprehension выполняется в C-ускоренном цикле списка."},
                    {"id": "opt2", "text": "Он не выделяет память", "isCorrect": False, "explanation": "Память он тоже выделяет."},
                    {"id": "opt3", "text": "Он не хранит результаты", "isCorrect": False, "explanation": "Хранит, в этом его смысл."}
                ],
                "hint": "Сравните количество операций в обоих циклах."
            },
            {
                "id": "q2",
                "question": "Зачем профилировать, а не гадать?",
                "options": [
                    {"id": "opt1", "text": "Данные показывают реальные узкие места", "isCorrect": True, "explanation": "cProfile/tracemalloc дают факты вместо догадок."},
                    {"id": "opt2", "text": "Чтобы код выглядел сложнее", "isCorrect": False, "explanation": "Не цель."},
                    {"id": "opt3", "text": "Это требование стиля", "isCorrect": False, "explanation": "Профилировка — про скорость, не стиль."}
                ],
                "hint": "Что надёжнее — измерение или предположение?"
            }
        ],
        "attachedTasks": [
            {"taskId": "30-p1", "title": "Список квадратов (comprehension)", "difficulty": "easy", "slug": "list-squares"},
            {"taskId": "30-p2", "title": "Дубликаты за O(n)", "difficulty": "medium", "slug": "count-duplicates"},
            {"taskId": "30-p3", "title": "Длина серии (память O(1))", "difficulty": "hard", "slug": "longest-run"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "list comprehension быстрее append-цикла из-за C-оптимизации.",
                "set-проверки дают O(1) «уже видели» вместо вложенного цикла O(n²).",
                "Профилируйте cProfile, а не гадайте, где узкое место.",
                "Алгоритм с памятью O(1) экономит ресурсы при больших данных."
            ]
        }
    },
    "problems": [
        {
            "id": "30-p1", "title": "Список квадратов (comprehension)", "difficulty": "easy",
            "lecture_id": "30", "order": 1, "entry_function": "list_squares",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def list_squares(n: int) -> list[int]:\n    \"\"\"Список квадратов 1..n через list comprehension.\"\"\"\n    ...",
            "description": "Напишите функцию `list_squares(n)`, возвращающую список квадратов `1,4,9,...,n²` при помощи **list comprehension** — это самый быстрый способ собрать список по формуле.\n\n**Функция решения:**\n\n```python\ndef list_squares(n: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "n = 3", "output": "[1,4,9]", "explanation": "1²,2²,3²."},
                {"input": "n = 1", "output": "[1]", "explanation": "Только 1²."}
            ],
            "constraints": ["1 ≤ n ≤ 10^4"],
            "hints": [
                "[i*i for i in range(1, n+1)].",
                "Comprehension быстрее цикла с append."
            ],
            "args": [
                [3], [1], [5], [0], [4], [10]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "30-p2", "title": "Дубликаты за O(n)", "difficulty": "medium",
            "lecture_id": "30", "order": 2, "entry_function": "count_duplicates",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "import collections\n\ndef count_duplicates(nums: list[int]) -> int:\n    \"\"\"Сколько различных чисел встречается в nums более одного раза (за O(n)).\"\"\"\n    ...",
            "description": "Дан список `nums`. Найдите **количество различных чисел, встречающихся более одного раза**, за `O(n)` времени (вложенный цикл — это и есть «узкое место», которое надо устранить).\n\n**Функция решения:**\n\n```python\ndef count_duplicates(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,2,2,3,3,3]", "output": "2", "explanation": "Дубликаты: 2 и 3 (3 встречается трижды — всё равно одно число)."},
                {"input": "nums = [1,2,3]", "output": "0", "explanation": "Повторов нет."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 10^5"],
            "hints": [
                "collections.Counter считает частоты за O(n).",
                "Сосчитайте значения > 1 — это дубликаты."
            ],
            "args": [
                [[1, 2, 2, 3, 3, 3]],
                [[1, 2, 3]],
                [[1, 1, 1]],
                [[4, 4, 5]],
                [[0, 0, 1, 1, 2]],
                [[9]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "30-p3", "title": "Длина серии (память O(1))", "difficulty": "hard",
            "lecture_id": "30", "order": 3, "entry_function": "longest_run_len",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def longest_run_len(nums: list[int]) -> int:\n    \"\"\"Длина самой длинной серии подряд идущих одинаковых значений (память O(1)).\"\"\"\n    ...",
            "description": "Реализуйте `longest_run_len(nums)`, возвращающую **длину самой длинной серии** подряд идущих одинаковых значений, используя только `O(1)` дополнительной памяти (никаких списков/словарей). Это и есть соревнование за память.\n\n**Функция решения:**\n\n```python\ndef longest_run_len(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,1,2,2,2,3]", "output": "3", "explanation": "Серия из трёх двоек."},
                {"input": "nums = []", "output": "0", "explanation": "Пустой список."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 10^5"],
            "hints": [
                "Два счётчика: текущая и лучшая длина серии.",
                "При смене значения сбрасывайте текущую длину в 1."
            ],
            "args": [
                [[1, 1, 2, 2, 2, 3]],
                [[]],
                [[5]],
                [[1, 2, 3, 4]],
                [[0, 0, 0]],
                [[1, 1, 2, 2, 1, 1, 1]]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])