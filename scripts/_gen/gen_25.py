"""Данные блока 25: Комбинаторика (подмножества, перестановки)."""
from genlib import run

LECTURE_SLUG = "25_combinations"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "25",
        "slug": "combinations",
        "title": "Комбинаторика и перебор",
        "description": "Комбинации, перестановки и подмножества — классика перебора. Разбираем сочетания через backtracking, все перестановки с откатом и генерацию подмножеств по битовым маскам.",
        "durationMinutes": 12,
        "difficulty": "middle",
        "tags": ["Algorithms", "Backtracking", "Combinations", "Combinatorics"],
        "learningOutcomes": [
            "Генерировать сочетания k из n без повторов",
            "Строить все перестановки с откатом (backtracking)",
            "Получать подмножества через битовые маски или рекурсию"
        ],
        "complexity": {
            "timeComplexity": "O(C(n,k) · k)",
            "spaceComplexity": "O(C(n,k) · k)",
            "explanation": "Число ответов — C(n,k) или n!, каждый требует O(k) памяти и времени на выдачу."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Почему для перестановок важен откат (backtrack)?",
                "options": [
                    {"id": "opt1", "text": "Освобождаем использованный элемент для следующих ветвей", "isCorrect": True, "explanation": "После рекурсивного возврата элемент снова доступен."},
                    {"id": "opt2", "text": "Он ускоряет сортировку", "isCorrect": False, "explanation": "Сортировка не связана."},
                    {"id": "opt3", "text": "Он уменьшает память ответа", "isCorrect": False, "explanation": "Память определяет число ответов."}
                ],
                "hint": "Что происходит с отметкой «использовано» после выхода из ветки?"
            },
            {
                "id": "q2",
                "question": "Сколько подмножеств у множества из n элементов?",
                "options": [
                    {"id": "opt1", "text": "2^n", "isCorrect": True, "explanation": "Каждый элемент входит или нет."},
                    {"id": "opt2", "text": "n^2", "isCorrect": False, "explanation": "n^2 меньше настоящего числа."},
                    {"id": "opt3", "text": "n!", "isCorrect": False, "explanation": "n! — число перестановок."}
                ],
                "hint": "Сколько вариантов выбора есть у каждого элемента?"
            }
        ],
        "attachedTasks": [
            {"taskId": "25-p1", "title": "Комбинации", "difficulty": "easy", "slug": "combinations"},
            {"taskId": "25-p2", "title": "Перестановки", "difficulty": "medium", "slug": "permutations"},
            {"taskId": "25-p3", "title": "Подмножества", "difficulty": "hard", "slug": "subsets"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Сочетание: выбираем индексы по возрастанию, без повторений.",
                "Перестановка: все порядки, откат отметок использованного.",
                "Подмножество: битовая маска от 0 до 2^n-1.",
                "Ответов всегда экспоненциально много."
            ]
        }
    },
    "problems": [
{
            "id": "25-p1", "title": "Комбинации", "difficulty": "easy",
            "lecture_id": "25", "order": 1, "entry_function": "combine",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def combine(n: int, k: int) -> list[list[int]]:\n    \"\"\"Все сочетания k чисел из [1..n] (порядок возрастания).\"\"\"\n    ...",
            "description": "Верните **все возможные комбинации** из `k` чисел, выбранных из диапазона `[1..n]`, в **возрастающем** порядке.\n\n**Функция решения:**\n\n```python\ndef combine(n: int, k: int) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "n = 4, k = 2", "output": "[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]", "explanation": "Все пары из {1,2,3,4}."},
                {"input": "n = 1, k = 1", "output": "[[1]]", "explanation": "Единственная комбинация."},
                {"input": "n = 3, k = 0", "output": "[[]]", "explanation": "Пустая комбинация."}
            ],
            "constraints": ["1 ≤ n ≤ 20", "0 ≤ k ≤ n"],
            "hints": [
                "Backtracking: на шаге i выбираем число от last+1 до n.",
                "Когда собрали k чисел — добавляем копию в ответ.",
                "Если k = 0 — ответ [[]]."
            ],
            "args": [
                [4, 2],
                [1, 1],
                [3, 0],
                [4, 3],
                [2, 1],
                [3, 4]
            ],
            "hidden": [False, False, True, True, True, True]
        },
# P1END
{
            "id": "25-p2", "title": "Перестановки", "difficulty": "medium",
            "lecture_id": "25", "order": 2, "entry_function": "permute",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def permute(nums: list[int]) -> list[list[int]]:\n    \"\"\"Все перестановки массива nums.\"\"\"\n    ...",
            "description": "Дан массив целых чисел `nums` с **различными** элементами. Верните **все возможные перестановки**.\n\n**Функция решения:**\n\n```python\ndef permute(nums: list[int]) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "nums = [1, 2, 3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]", "explanation": "Все 6 перестановок."},
                {"input": "nums = [0, 1]", "output": "[[0,1],[1,0]]", "explanation": "Две перестановки."},
                {"input": "nums = [1]", "output": "[[1]]", "explanation": "Одна перестановка."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 6", "Все элементы различны"],
            "hints": [
                "Отслеживайте использованные индексы.",
                "После рекурсивного спуска откатывайте выбор.",
                "Копируйте текущий путь в ответ при полной длине."
            ],
            "args": [
                [1, 2, 3],
                [0, 1],
                [1],
                []
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True]
        },
# P2END
{
            "id": "25-p3", "title": "Подмножества", "difficulty": "hard",
            "lecture_id": "25", "order": 3, "entry_function": "subsets",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def subsets(nums: list[int]) -> list[list[int]]:\n    \"\"\"Все подмножества массива nums (включая пустое).\"\"\"\n    ...",
            "description": "Дан массив целых чисел `nums` с **различными** элементами. Верните **все возможные подмножества** (включая пустое), без дубликатов.\n\n**Функция решения:**\n\n```python\ndef subsets(nums: list[int]) -> list[list[int]]:\n    ...\n```",
            "examples": [
                {"input": "nums = [1, 2]", "output": "[[], [1], [2], [1, 2]]", "explanation": "4 подмножества."},
                {"input": "nums = [0]", "output": "[[], [0]]", "explanation": "Пустое и само число."},
                {"input": "nums = []", "output": "[[]]", "explanation": "Только пустое множество."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 10", "Все элементы различны", "|nums[i]| ≤ 10"],
            "hints": [
                "Перебирайте битовые маски от 0 до 2^n - 1.",
                "Бит i указывает, входит ли nums[i] в подмножество.",
                "Каждой маске соответствует одно подмножество."
            ],
            "args": [
                [1, 2, 3],
                [1, 2],
                [0],
                []
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])
# EOF