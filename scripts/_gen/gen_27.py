"""Данные блока 27: Itertools (работа с итераторами)."""
from genlib import run

LECTURE_SLUG = "27_itertools"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "27",
        "slug": "itertools",
        "title": "Itertools: комбинаторика и ленивые итераторы",
        "description": "Модуль itertools даёт быстрые и ленивые итераторы: product, permutations, combinations, chain, cycle и другие. Разбираем комбинаторные задачи и построение повторяющихся последовательностей.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Standard Library", "Iterators", "Combinatorics"],
        "learningOutcomes": [
            "Генерировать сочетания и произведения через product/combinations",
            "Дедуплицировать элементы, сохраняя порядок обхода",
            "Строить циклические последовательности через cycle/islice"
        ],
        "complexity": {
            "timeComplexity": "O(C(n,k)) для комбинаторики",
            "spaceComplexity": "O(1) на шаг итератора (лениво)",
            "explanation": "Итераторы itertools работают лениво — память O(1) на шаг, но объём результата комбинаторного взрыва влияет на время."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что вернёт product('AB', range(2))?",
                "options": [
                    {"id": "opt1", "text": "('A',0),('A',1),('B',0),('B',1)", "isCorrect": True, "explanation": "Декартово произведение в лексикографическом порядке."},
                    {"id": "opt2", "text": "['AB','A0','B1']", "isCorrect": False, "explanation": "Это не кортежи произведения."},
                    {"id": "opt3", "text": "('A','B'),('0','1')", "isCorrect": False, "explanation": "Кортежи из одного элемента каждого списка."}
                ],
                "hint": "Как устроено декартово произведение?"
            },
            {
                "id": "q2",
                "question": "Чем отличаются combinations и permutations?",
                "options": [
                    {"id": "opt1", "text": "В permutations важен порядок элементов", "isCorrect": True, "explanation": "permutations учитывает порядок, combinations — нет."},
                    {"id": "opt2", "text": "Они полностью идентичны", "isCorrect": False, "explanation": "Порядок внутри набора различает их."},
                    {"id": "opt3", "text": "combinations больше по размеру", "isCorrect": False, "explanation": "permutations больше: n!/(n-k)! против C(n,k)."}
                ],
                "hint": "Меняют ли местами элементы внутри набора?"
            }
        ],
        "attachedTasks": [
            {"taskId": "27-p1", "title": "Комбинации", "difficulty": "easy", "slug": "combinations"},
            {"taskId": "27-p2", "title": "Произведение списков", "difficulty": "medium", "slug": "cartesian-product"},
            {"taskId": "27-p3", "title": "Циклическая последовательность", "difficulty": "hard", "slug": "cyclic-sequence"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "product(*lists) — декартово произведение; dedup через set с сохранением порядка.",
                "combinations(nums, k) — сочетания без учёта порядка; permutations — с учётом.",
                "cycle(it) + islice(it, n) — бесконечная циклическая последовательность.",
                "chain(*its) склеивает итераторы; zip_longest — с fillvalue.",
                "Итераторы ленивые: память O(1) на шаг."
            ]
        }
    },
    "problems": [
        {
            "id": "27-p1", "title": "Комбинации", "difficulty": "easy",
            "lecture_id": "27", "order": 1, "entry_function": "combinations",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def combinations(nums: list[int], k: int) -> list[list[int]]:\n    \"\"\"Вернуть все сочетания по k элементов (без учёта порядка).\"\"\"\n    ...",
            "description": "Дан массив `nums` (элементы попарно различны) и число `k`. Верните все **сочетания** по `k` элементов. Порядок элементов внутри набора и порядок наборов не важен.\n\n**Функция решения:**\n\n```python\ndef combinations(nums: list[int], k: int) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,2,3,4], k = 2", "output": "[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]", "explanation": "Все пары элементов."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 15", "0 ≤ k ≤ len(nums)"],
            "hints": [
                "itertools.combinations(nums, k) вернёт все сочетания.",
                "Для эталона можно использовать combinations из стандартной библиотеки."
            ],
            "sort_result": True,
            "args": [
                [[1, 2, 3, 4], 2],
                [[1, 2], 1],
                [[1, 2, 3], 3],
                [[5, 6, 7], 2],
                [[1], 0],
                [[1, 2, 3, 4, 5], 3],
                [[9, 8], 2]
            ],
            "hidden": [False, False, True, True, False, True, True]
        },
        {
            "id": "27-p2", "title": "Произведение списков", "difficulty": "medium",
            "lecture_id": "27", "order": 2, "entry_function": "cartesian_product",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def cartesian_product(lists: list[list[int]]) -> list[list[int]]:\n    \"\"\"Вернуть декартово произведение списков без повторяющихся кортежей.\"\"\"\n    ...",
            "description": "Дан список списков `lists`. Верните **всевозможные кортежи** декартова произведения их элементов через `itertools.product`, убрав повторяющиеся кортежи (порядок — как при обходе product).\n\n**Функция решения:**\n\n```python\ndef cartesian_product(lists: list[list[int]]) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "lists = [[1,2],[3,4]]", "output": "[[1,3],[1,4],[2,3],[2,4]]", "explanation": "Декартово произведение в порядке product(*lists)."}
            ],
            "constraints": ["1 ≤ len(lists) ≤ 8", "1 ≤ len(списка) ≤ 8"],
            "hints": [
                "product(*lists) даёт все комбинации; для дедупликации ведите set виденных кортежей.",
                "Сохраняйте порядок обхода product, а не сортируйте результат."
            ],
            "args": [
                [[[1, 2], [3, 4]]],
                [[[1], [2], [3]]],
                [[[1, 2], [1, 2]]],
                [[[], [1, 2]]],
                [[[1, 2, 3], [7]]],
                [[["a", "b"], ["c"]]],
                [[[0]]]
            ],
            "hidden": [False, True, False, True, True, True, True]
        },
        {
            "id": "27-p3", "title": "Циклическая последовательность", "difficulty": "hard",
            "lecture_id": "27", "order": 3, "entry_function": "cyclic_sequence",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def cyclic_sequence(n: int, count: int) -> list[int]:\n    \"\"\"Первые count значений бесконечного цикла 0,1,...,n-1,0,1,...\"\"\"\n    ...",
            "description": "Постройте **бесконечную** последовательность `0,1,...,n-1,0,1,...` и верните её **первые `count`** значений. Реализуйте через `itertools.cycle` и `islice` (или вручную через генератор).\n\n**Функция решения:**\n\n```python\ndef cyclic_sequence(n: int, count: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "n = 4, count = 7", "output": "[0,1,2,3,0,1,2]", "explanation": "Цикл 0..3 повторяется."},
                {"input": "n = 2, count = 3", "output": "[0,1,0]", "explanation": "Повтор 0,1."}
            ],
            "constraints": ["1 ≤ n ≤ 1000", "0 ≤ count ≤ 10^5"],
            "hints": [
                "itertools.cycle(range(n)) — бесконечный цикл.",
                "itertools.islice(cycle_it, count) возьмёт первые count значений."
            ],
            "args": [
                [4, 7],
                [2, 3],
                [3, 0],
                [1, 5],
                [5, 9],
                [10, 15],
                [6, 2]
            ],
            "hidden": [False, False, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])