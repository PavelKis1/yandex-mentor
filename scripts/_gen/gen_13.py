"""Данные блока 13: Динамическое программирование (1D)."""
from genlib import run

LECTURE_SLUG = "13_dp_1d"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "13",
        "slug": "dp-1d",
        "title": "Динамическое программирование: 1D (DP 1D)",
        "description": "Динамическое программирование решает задачу через переиспользование решений меньших подзадач. Рассматриваем одномерные переходы: подъём по лестнице, максимальная сумма без соседей, минимальное число монет.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "Dynamic Programming", "Optimization"],
        "learningOutcomes": [
            "Выводить рекуррентное соотношение из описания задачи",
            "Реализовывать итеративное DP с константной памятью точечных переходов",
            "Инициализировать DP-массив и обрабатывать недостижимые состояния"
        ],
        "complexity": {
            "timeComplexity": "O(n) / O(n * C)",
            "spaceComplexity": "O(1) или O(n)",
            "explanation": "Одномерные переходы сводят задачу к проходу по массиву; память можно сжать до пары переменных, если переход зависит только от предыдущих шагов."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что обязательно задать при построении рекуррентного соотношения?",
                "options": [
                    {"id": "opt1", "text": "Базовые случаи (dp[0], dp[1]) и правило перехода", "isCorrect": True, "explanation": "Без базы и перехода рекуррентность не определена."},
                    {"id": "opt2", "text": "Сложность O(1) для всех задач", "isCorrect": False, "explanation": "Память и время зависят от задачи."},
                    {"id": "opt3", "text": "Использование рекурсии как обязательного приёма", "isCorrect": False, "explanation": "Рекурсия необязательна — чаще итеративно."}
                ],
                "hint": "С чего начинается построение любой DP?"
            },
            {
                "id": "q2",
                "question": "Какой признак задачи подсказывает применить 1D DP?",
                "options": [
                    {"id": "opt1", "text": "Решение зависит от одного линейного параметра (например, суммы или позиции)", "isCorrect": True, "explanation": "Один параметр → массив размером O(n)."},
                    {"id": "opt2", "text": "Данные всегда отсортированы", "isCorrect": False, "explanation": "Сортировка не критерий DP."},
                    {"id": "opt3", "text": "Нужно найти любой элемент массива", "isCorrect": False, "explanation": "Это поиск, а не оптимизация."}
                ],
                "hint": "Сколько независимых параметров задают состояние?"
            }
        ],
        "attachedTasks": [
            {"taskId": "13-p1", "title": "Лестница", "difficulty": "easy", "slug": "climbing-stairs"},
            {"taskId": "13-p2", "title": "Грабитель", "difficulty": "medium", "slug": "house-robber"},
            {"taskId": "13-p3", "title": "Монеты", "difficulty": "hard", "slug": "coin-change"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Определите параметр-состояние (позиция, сумма) и базу dp[0].",
                "Выпишите переход: dp[i] = f(dp[i-1], dp[i-2], инкремент).",
                "Порядок вычисления — от меньших индексов к большим.",
                "Сжимайте память: если нужны только 2 предыдущих значения, храните две переменные.",
                "Недостижимые состояния помечайте отдельно (+∞ / -1)."
            ]
        }
    },
    "problems": [
{
            "id": "13-p1", "title": "Лестница", "difficulty": "easy",
            "lecture_id": "13", "order": 1, "entry_function": "climb_stairs",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def climb_stairs(n: int) -> int:\n    \"\"\"Количество способов подняться на n ступеней (шаги 1 или 2).\"\"\"\n    ...",
            "description": "Вы поднимаетесь по лестнице из `n` ступеней. За один раз можно сделать **1** или **2** шага. Верните **количество различных способов** подняться на вершину. Если `n <= 0`, верните 0.\n\n**Функция решения:**\n\n```python\ndef climb_stairs(n: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "n = 3", "output": "3", "explanation": "Способы: 1+1+1, 1+2, 2+1."},
                {"input": "n = 4", "output": "5", "explanation": "Числа Фибоначчи: 1, 2, 3, 5."},
                {"input": "n = 0", "output": "0", "explanation": "Подниматься не нужно — 0 способов."}
            ],
            "constraints": ["0 ≤ n ≤ 45", "Допустимые шаги: 1 и 2"],
            "hints": [
                "dp[n] = dp[n-1] + dp[n-2] — это числа Фибоначчи.",
                "Достаточно хранить два последних значения: a, b."
            ],
            "args": [[1], [2], [3], [4], [5], [0], [-3], [10]],
            "hidden": [False, False, False, True, True, False, True, True]
        },
        {
            "id": "13-p2", "title": "Грабитель", "difficulty": "medium",
            "lecture_id": "13", "order": 2, "entry_function": "rob",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def rob(nums: list[int]) -> int:\n    \"\"\"Максимальная сумма, не беря соседние элементы.\"\"\"\n    ...",
            "description": "Вдоль улицы стоят дома, в `nums[i]` — ценности. Грабитель не может ограбить два **соседних** дома. Верните максимальную сумму, которую можно украсть.\n\n**Функция решения:**\n\n```python\ndef rob(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [2, 7, 9, 3, 1]", "output": "12", "explanation": "Грабим дома 0, 2, 4: 2+9+1=12."},
                {"input": "nums = [2, 1, 1, 2]", "output": "4", "explanation": "Грабим дома 0 и 3: 2+2=4."},
                {"input": "nums = []", "output": "0", "explanation": "Домов нет."}
            ],
            "constraints": ["0 ≤ len(nums) ≤ 10^5", "0 ≤ nums[i] ≤ 10^4"],
            "hints": [
                "dp[i] = max(ограбить i, пропустить i) = max(prev + nums[i], curr).",
                "Храните только два значения: curr и prev."
            ],
            "args": [[[2, 1, 1, 2]], [[2, 7, 9, 3, 1]], [[1, 2]], [[1, 2, 3, 1]], [[5, 3, 4, 11, 2]], [[0, 0, 0, 0]], [[]], [[3, 2, 3, 4]]],
            "hidden": [True, False, False, False, True, True, False, True]
        },
        {
            "id": "13-p3", "title": "Монеты", "difficulty": "hard",
            "lecture_id": "13", "order": 3, "entry_function": "coin_change",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def coin_change(coins: list[int], amount: int) -> int:\n    \"\"\"Минимальное число монет для суммы amount или -1.\"\"\"\n    ...",
            "description": "Даны номиналы монет `coins` (каждую можно использовать неограниченно) и сумма `amount`. Верните **минимальное количество монет**, которыми можно составить `amount`, или `-1`, если это невозможно.\n\n**Функция решения:**\n\n```python\ndef coin_change(coins: list[int], amount: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "coins = [1, 2, 5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1 (3 монеты)."},
                {"input": "coins = [2], amount = 3", "output": "-1", "explanation": "Нельзя составить 3 из двоек."},
                {"input": "coins = [1], amount = 0", "output": "0", "explanation": "Сумма 0 — ноль монет."}
            ],
            "constraints": ["1 ≤ len(coins) ≤ 12", "1 ≤ coins[i] ≤ 2^31 - 1", "0 ≤ amount ≤ 10^4"],
            "hints": [
                "dp[a] = min(dp[a - c] + 1) по всем монетам c ≤ a.",
                "Инициализируйте dp[0] = 0, остальные — значением 'плюс бесконечность'.",
                "Если dp[amount] остался бесконечным — верните -1."
            ],
            "args": [[[1, 2, 5], 11], [[2], 3], [[1], 0], [[1, 5, 10, 25], 30], [[2], 1], [[186, 419, 83, 408], 6249], [[1, 2, 3], 4], [[3], 5]],
            "hidden": [False, False, False, False, True, True, False, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])