"""Данные блока 16: Перебор (Backtracking)."""
from genlib import run

LECTURE_SLUG = "16_backtracking"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "16",
        "slug": "backtracking",
        "title": "Перебор и откат (Backtracking)",
        "description": "Backtracking систематически перебирает решения, делая выбор на каждом шаге и откатывая его при тупике. Разбираем перестановки, подмножества и задачу о N ферзях.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "Backtracking", "Recursion"],
        "learningOutcomes": [
            "Строить дерево решений и выражать его рекурсией",
            "Корректно добавлять и откатывать выбранное состояние",
            "Оценивать сложность экспоненциального перебора"
        ],
        "complexity": {
            "timeComplexity": "O(n!) / O(2^n)",
            "spaceComplexity": "O(n) (глубина рекурсии)",
            "explanation": "Перестановок n!, подмножеств 2^n; глубина рекурсии равна числу выбранных элементов."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что обязательно сделать после рекурсивного вызова в backtracking?",
                "options": [
                    {"id": "opt1", "text": "Откатить изменения (убрать выбранный элемент)", "isCorrect": True, "explanation": "Иначе состояние «загрязняется» для следующей ветки."},
                    {"id": "opt2", "text": "Перезапустить программу", "isCorrect": False, "explanation": "Откат должен быть на уровне алгоритма."},
                    {"id": "opt3", "text": "Отсортировать входные данные", "isCorrect": False, "explanation": "Сортировка не всегда нужна и не заменяет откат."}
                ],
                "hint": "Как вернуть дерево решений к исходному состоянию?"
            },
            {
                "id": "q2",
                "question": "Сколько существует подмножеств множества из n элементов?",
                "options": [
                    {"id": "opt1", "text": "2^n", "isCorrect": True, "explanation": "Каждый элемент либо входит, либо нет."},
                    {"id": "opt2", "text": "n^2", "isCorrect": False, "explanation": "Так считаются пары, не подмножества."},
                    {"id": "opt3", "text": "n!", "isCorrect": False, "explanation": "n! — число перестановок, не подмножеств."}
                ],
                "hint": "Сколько бинарных вариантов у каждого элемента?"
            }
        ],
        "attachedTasks": [
            {"taskId": "16-p1", "title": "Перестановки", "difficulty": "easy", "slug": "permutations"},
            {"taskId": "16-p2", "title": "Подмножества", "difficulty": "medium", "slug": "subsets"},
            {"taskId": "16-p3", "title": "N-Queens", "difficulty": "hard", "slug": "n-queens"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Опишите выбор на каждом шаге (какую фигуру/символ взять).",
                "Рекурсия = переход к следующему уровню с учётом сделанного выбора.",
                "Откатывайте выбор после рекурсивного вызова.",
                "Используйте множества/массивы для проверки ограничений за O(1).",
                "Помните: перебор экспоненциальный — важны оптимизации и ограничения."
            ]
        }
    },
    "problems": [
{
            "id": "16-p1", "title": "Перестановки", "difficulty": "easy",
            "lecture_id": "16", "order": 1, "entry_function": "permute",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def permute(nums: list[int]) -> list[list[int]]:\n    \"\"\"Все перестановки массива nums.\"\"\"\n    ...",
            "description": "Дан массив целых чисел `nums` с **различными** элементами. Верните **все возможные перестановки**. Порядок результатов не важен, но должен совпадать с эталоном.\n\n**Функция решения:**\n\n```python\ndef permute(nums: list[int]) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "nums = [0, 1]", "output": "[[0, 1], [1, 0]]", "explanation": "Две перестановки."},
                {"input": "nums = [1, 2, 3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "explanation": "3! = 6 перестановок."},
                {"input": "nums = []", "output": "[[]]", "explanation": "Пустое множество даёт одну пустую перестановку."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 6", "Все элементы nums различны"],
            "hints": [
                "Каждый шаг выбирайте неиспользованный элемент.",
                "Отслеживайте использованные индексы и откатывайте выбор."
            ],
            "args": [[[0, 1]], [[1, 2, 3]], [[]], [[1]], [[1, 2]]],
            "hidden": [False, False, True, True, True]
        },
        {
            "id": "16-p2", "title": "Подмножества", "difficulty": "medium",
            "lecture_id": "16", "order": 2, "entry_function": "subsets",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def subsets(nums: list[int]) -> list[list[int]]:\n    \"\"\"Все подмножества массива nums.\"\"\"\n    ...",
            "description": "Дан массив целых чисел `nums` с **различными** элементами. Верните **все возможные подмножества** (включая пустое), без дубликатов.\n\n**Функция решения:**\n\n```python\ndef subsets(nums: list[int]) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "nums = [1, 2]", "output": "[[], [1], [1, 2], [2]]", "explanation": "4 подмножества."},
                {"input": "nums = [1, 2, 3]", "output": "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]", "explanation": "2^3 = 8 подмножеств."},
                {"input": "nums = []", "output": "[[]]", "explanation": "Только пустое множество."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 10", "Все элементы nums различны"],
            "hints": [
                "Для каждого элемента есть два пути: включить или пропустить.",
                "Можно перебирать битовые маски от 0 до 2^n - 1."
            ],
            "args": [[[]], [[1]], [[1, 2]], [[1, 2, 3]]],
            "hidden": [True, True, False, False]
        },
        {
            "id": "16-p3", "title": "N-Queens", "difficulty": "hard",
            "lecture_id": "16", "order": 3, "entry_function": "solve_n_queens",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def solve_n_queens(n: int) -> list[list[str]]:\n    \"\"\"Все расстановки n ферзей на доске n x n ('Q' и '.').\"\"\"\n    ...",
            "description": "Разместите `n` ферзей на доске `n x n` так, чтобы они не били друг друга (по горизонтали, вертикали и диагоналям). Верните **все конфигурации** доски в виде списка строк ('Q' — ферзь, '.' — пусто). Порядок аналогичен эталонному.\n\n**Функция решения:**\n\n```python\ndef solve_n_queens(n: int) -> list[list[str]]:\n    ...\n```",
            "examples": [
                {"input": "n = 4", "output": "2 решения", "explanation": "Для доски 4x4 существует ровно 2 расстановки."},
                {"input": "n = 1", "output": "[[\"Q\"]]", "explanation": "Один ферзь на доске 1x1."},
                {"input": "n = 2", "output": "[]", "explanation": "На доске 2x2 ферзи поставить нельзя."}
            ],
            "constraints": ["0 ≤ n ≤ 9", "Ферзи не должны бить друг друга"],
            "hints": [
                "Строки перебирайте сверху вниз — ферзь один на строку.",
                "Проверяйте занятость по колонке и двум диагоналям за O(1)."
            ],
            "args": [[0], [1], [2], [3], [4]],
            "hidden": [True, True, False, True, False]
        }
    ]
}

if __name__ == "__main__":
    run([meta])