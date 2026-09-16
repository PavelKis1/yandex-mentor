"""Данные блока 23: Побитовые операции."""
from genlib import run

LECTURE_SLUG = "23_bitwise"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "23",
        "slug": "bitwise",
        "title": "Побитовые операции",
        "description": "Битовые трюки дают элегантные решения за O(n) и O(1) памяти. Разбираем одиночный элемент через XOR, подсчёт единичных битов и сложение чисел без + и - через XOR с переносом.",
        "durationMinutes": 12,
        "difficulty": "middle",
        "tags": ["Algorithms", "Bit Manipulation", "XOR", "Math"],
        "learningOutcomes": [
            "Использовать XOR для поиска непарного элемента",
            "Считать единичные биты за O(n) по DP-рекурсии",
            "Складывать числа через XOR (сумма) и AND<<1 (перенос)",
            "Держать в уме 32-битное маскирование для отрицательных чисел"
        ],
        "complexity": {
            "timeComplexity": "O(n)",
            "spaceComplexity": "O(1)",
            "explanation": "XOR-свёртка, счёт битов и битовая сумма работают за линейное время с константной памятью."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Почему XOR всех элементов находит одиночный элемент?",
                "options": [
                    {"id": "opt1", "text": "Парные значения сокращаются (x ^ x = 0)", "isCorrect": True, "explanation": "Каждая пара обнуляется, остаётся одиночный."},
                    {"id": "opt2", "text": "XOR сортирует массив", "isCorrect": False, "explanation": "XOR не сортирует."},
                    {"id": "opt3", "text": "XOR всегда возвращает максимум", "isCorrect": False, "explanation": "XOR — не максимум."}
                ],
                "hint": "Чему равно x ^ x?"
            },
            {
                "id": "q2",
                "question": "Как получить бит суммы без оператора +?",
                "options": [
                    {"id": "opt1", "text": "a ^ b — сумма без переноса, (a & b) << 1 — перенос", "isCorrect": True, "explanation": "Повторяем, пока перенос не станет 0."},
                    {"id": "opt2", "text": "a | b даёт сумму", "isCorrect": False, "explanation": "ИЛИ теряет переносы."},
                    {"id": "opt3", "text": "a << b", "isCorrect": False, "explanation": "Сдвиг — это умножение, не сложение."}
                ],
                "hint": "Какие два битовых результата дают XOR и AND сдвиг?"
            }
        ],
        "attachedTasks": [
            {"taskId": "23-p1", "title": "Один элемент", "difficulty": "easy", "slug": "single-number"},
            {"taskId": "23-p2", "title": "Количество бит", "difficulty": "medium", "slug": "counting-bits"},
            {"taskId": "23-p3", "title": "Сумма двух чисел", "difficulty": "hard", "slug": "sum-of-two-integers"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "x ^ x = 0, x ^ 0 = x — основа всех приёмов.",
                "Одиночный элемент: XOR всего массива.",
                "count_bits[i] = count_bits[i>>1] + (i&1).",
                "Сумма: a^b плюс перенос (a&b)<<1, повтор до 0.",
                "Для отрицательных — маска 32 бита + перевод в знаковое."
            ]
        }
    },
    "problems": [
{
            "id": "23-p1", "title": "Один элемент", "difficulty": "easy",
            "lecture_id": "23", "order": 1, "entry_function": "single_number",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def single_number(nums: list[int]) -> int:\n    \"\"\"Единственный элемент, который встречается один раз (остальные — по два).\"\"\"\n    ...",
            "description": "В массиве `nums` каждый элемент встречается **дважды**, кроме одного. Найдите **тот единственный** элемент.\n\n**Функция решения:**\n\n```python\ndef single_number(nums: list[int]) -> int:\n    ...\n```",
            "examples": [
                {"input": "nums = [2, 2, 1]", "output": "1", "explanation": "1 встречается один раз."},
                {"input": "nums = [4, 1, 2, 1, 2]", "output": "4", "explanation": "4 — единственный неповторяющийся."},
                {"input": "nums = [1]", "output": "1", "explanation": "Один элемент."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 3·10^4", "-3·10^4 ≤ nums[i] ≤ 3·10^4"],
            "hints": [
                "XOR двух одинаковых чисел равен 0.",
                "Проксорьте весь массив — останется искомый элемент.",
                "Работает и с отрицательными числами."
            ],
            "args": [
                [2, 2, 1],
                [4, 1, 2, 1, 2],
                [1],
                [-5, -5, 3],
                [7, 9, 9]
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True, True]
        },
# P1END
{
            "id": "23-p2", "title": "Количество бит", "difficulty": "medium",
            "lecture_id": "23", "order": 2, "entry_function": "count_bits",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def count_bits(n: int) -> list[int]:\n    \"\"\"ans[i] — количество единичных битов в i, для i от 0 до n.\"\"\"\n    ...",
            "description": "Для целого `n >= 0` верните массив `ans` длины `n+1`, где `ans[i]` — **количество единичных битов** в двоичном представлении `i`.\n\n**Функция решения:**\n\n```python\ndef count_bits(n: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "n = 2", "output": "[0, 1, 1]", "explanation": "0→0 бит, 1→1 бит, 2→1 бит."},
                {"input": "n = 5", "output": "[0, 1, 1, 2, 1, 2]", "explanation": "3=11 (2 бита), 5=101 (2 бита)."},
                {"input": "n = 0", "output": "[0]", "explanation": "Пустой диапазон."}
            ],
            "constraints": ["0 ≤ n ≤ 10^5"],
            "hints": [
                "Используйте: count[i] = count[i >> 1] + (i & 1).",
                "i>>1 отбрасывает младший бит; (i&1) добавляет его."
            ],
            "args": [
                2,
                5,
                0,
                1,
                8
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True, True]
        },
# P2END
{
            "id": "23-p3", "title": "Сумма двух чисел", "difficulty": "hard",
            "lecture_id": "23", "order": 3, "entry_function": "get_sum",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def get_sum(a: int, b: int) -> int:\n    \"\"\"Сумма a+b без использования операторов + и -.\"\"\"\n    ...",
            "description": "Верните сумму `a + b`, **не используя** операторы `+` и `-`. Числа целые, допускаются отрицательные.\n\n**Функция решения:**\n\n```python\ndef get_sum(a: int, b: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "a = 1, b = 2", "output": "3", "explanation": "Простое сложение."},
                {"input": "a = -1, b = 1", "output": "0", "explanation": "Взаимно уничтожаются."},
                {"input": "a = -2, b = -3", "output": "-5", "explanation": "Оба отрицательных."}
            ],
            "constraints": ["-1000 ≤ a, b ≤ 1000", "Работа в 32-битной арифметике"],
            "hints": [
                "a ^ b — сумма битов без переноса.",
                "(a & b) << 1 — перенос; повторяйте, пока перенос не 0.",
                "Маскируйте 32 бита, чтобы обработать отрицательные без зацикливания."
            ],
            "args": [
                [1, 2],
                [2, 3],
                [0, 0],
                [-1, 1],
                [-2, -3],
                [10, 7]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])
# EOF