"""Данные блока 26: Collections (специализированные контейнеры)."""
from genlib import run

LECTURE_SLUG = "26_collections"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "26",
        "slug": "collections",
        "title": "Collections: специализированные контейнеры",
        "description": "Модуль collections расширяет встроенные структуры: Counter — подсчёт, defaultdict — значения по умолчанию, deque — двусторонняя очередь за O(1). Разбираем классические задачи на частые элементы, анаграммы и палиндромы.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Standard Library", "Data Structures"],
        "learningOutcomes": [
            "Использовать Counter для подсчёта и top-K частых элементов",
            "Группировать данные через defaultdict по сортированному ключу",
            "Применять deque для задач на палиндромы за O(1) с обоих концов"
        ],
        "complexity": {
            "timeComplexity": "O(n) или O(n log k)",
            "spaceComplexity": "O(n)",
            "explanation": "Counter строит частотную таблицу за O(n), most_common(k) — O(n log k); deque даёт O(1) на операцию с обоих концов."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что удобнее всего для подсчёта частот элементов?",
                "options": [
                    {"id": "opt1", "text": "collections.Counter", "isCorrect": True, "explanation": "Counter — подкласс dict, готов к подсчёту и top-K."},
                    {"id": "opt2", "text": "обычный set", "isCorrect": False, "explanation": "set хранит только факт наличия, не частоту."},
                    {"id": "opt3", "text": "deque", "isCorrect": False, "explanation": "deque — очередь, а не счётчик."}
                ],
                "hint": "Какой словарь умеет most_common()?"
            },
            {
                "id": "q2",
                "question": "Какая сложность appendleft() у deque?",
                "options": [
                    {"id": "opt1", "text": "O(1)", "isCorrect": True, "explanation": "deque реализован как двухсвязный список блоков — O(1) с обоих концов."},
                    {"id": "opt2", "text": "O(n)", "isCorrect": False, "explanation": "O(n) было бы у list.insert(0, ...)."},
                    {"id": "opt3", "text": "O(log n)", "isCorrect": False, "explanation": "Логарифмической сложности у очереди нет."}
                ],
                "hint": "Почему deque создавали именно для этого?"
            }
        ],
        "attachedTasks": [
            {"taskId": "26-p1", "title": "Топ K частых элементов", "difficulty": "easy", "slug": "top-k-frequent"},
            {"taskId": "26-p2", "title": "Группа анаграмм", "difficulty": "medium", "slug": "group-anagrams"},
            {"taskId": "26-p3", "title": "Палиндром с deque", "difficulty": "hard", "slug": "valid-palindrome"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Counter(nums).most_common(k) — топ-K частых элементов за O(n log k).",
                "Ключ анаграммы — tuple(sorted(s)) или frozenset Counter.",
                "deque: append/pop с обоих концов за O(1); popleft() для палиндрома.",
                "defaultdict(int/list) избавляет от проверок существования ключа.",
                "namedtuple — лёгкие иммутабельные контейнеры с именованными полями."
            ]
        }
    },
    "problems": [
        {
            "id": "26-p1", "title": "Топ K частых элементов", "difficulty": "easy",
            "lecture_id": "26", "order": 1, "entry_function": "top_k_frequent",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def top_k_frequent(nums: list[int], k: int) -> list[int]:\n    \"\"\"Вернуть k наиболее частых элементов. Порядок не важен.\"\"\"\n    ...",
            "description": "Дан массив `nums` и число `k`. Верните **k наиболее часто встречающихся** элементов. Порядок элементов в ответе не важен.\n\n**Функция решения:**\n\n```python\ndef top_k_frequent(nums: list[int], k: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]", "explanation": "1 встречается 3 раза, 2 — два раза."},
                {"input": "nums = [1], k = 1", "output": "[1]", "explanation": "Единственный элемент."}
            ],
            "constraints": ["1 ≤ len(nums) ≤ 10^5", "1 ≤ k ≤ число различных элементов"],
            "hints": [
                "collections.Counter(nums).most_common(k) вернёт пары (элемент, частота).",
                "Возьмите только элементы из первых k пар."
            ],
            "sort_result": True,
            "args": [
                [[1, 1, 1, 2, 2, 3], 2],
                [[1], 1],
                [[1, 2, 2, 3, 3, 3], 2],
                [[3, 0, 1, 0], 1],
                [[1, 2, 3], 3],
                [[1, 1, 2, 2], 1],
                [[4, 4, 4, 4], 1]
            ],
            "hidden": [False, False, True, True, False, True, True]
        },
        {
            "id": "26-p2", "title": "Группа анаграмм", "difficulty": "medium",
            "lecture_id": "26", "order": 2, "entry_function": "group_anagrams",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def group_anagrams(strs: list[str]) -> list[list[str]]:\n    \"\"\"Сгруппировать слова-анаграммы. Порядок групп и слов не важен.\"\"\"\n    ...",
            "description": "Дан массив строк `strs`. Сгруппируйте **анаграммы** (строки, составленные из одного набора букв) в один список. Группу может образовывать и одна строка. Порядок групп и слов внутри не важен.\n\n**Функция решения:**\n\n```python\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ...\n```",
            "examples": [
                {"input": "strs = ['eat','tea','tan','ate','nat','bat']", "output": "[['bat'],['nat','tan'],['ate','eat','tea']]", "explanation": "eat/tea/ate — анаграммы, tan/nat — анаграммы."}
            ],
            "constraints": ["1 ≤ len(strs) ≤ 10^4", "0 ≤ len(s) ≤ 100"],
            "hints": [
                "Ключ группы — отсортированная строка или tuple(sorted(s)).",
                "defaultdict(list) накапливает строки с одинаковым ключом."
            ],
            "sort_result": True,
            "args": [
                [["eat", "tea", "tan", "ate", "nat", "bat"]],
                [["a"]],
                [["bddddddddd", "bbbbbbbbdd"]],
                [["abc", "cba", "bac", "d", "d"]],
                [["listen", "silent", "enlist", "hello"]],
                [[""]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "26-p3", "title": "Палиндром с deque", "difficulty": "hard",
            "lecture_id": "26", "order": 3, "entry_function": "is_palindrome",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def is_palindrome(s: str) -> bool:\n    \"\"\"Проверить палиндром, учитывая только буквы/цифры и игнорируя регистр.\"\"\"\n    ...",
            "description": "Дана строка `s`. Проверьте, является ли она **палиндромом**: учитываются только буквы и цифры, регистр игнорируется. Рекомендуется реализация через `collections.deque` — сравнение с обоих концов.\n\n**Функция решения:**\n\n```python\ndef is_palindrome(s: str) -> bool:\n    ...\n```",
            "examples": [
                {"input": "s = 'A man, a plan, a canal: Panama'", "output": "True", "explanation": "'amanaplanacanalpanama' — палиндром."},
                {"input": "s = 'race a car'", "output": "False", "explanation": "'raceacar' не палиндром."},
                {"input": "s = ' '", "output": "True", "explanation": "Пустая строка считается палиндромом."}
            ],
            "constraints": ["1 ≤ len(s) ≤ 2·10^5"],
            "hints": [
                "deque: постройте очередь из отфильтрованных символов в lower().",
                "Сравнивайте popleft() и pop() — если хоть раз не равны, верните False."
            ],
            "args": [
                ["A man, a plan, a canal: Panama"],
                ["race a car"],
                [" "],
                ["ab_a"],
                ["0P"],
                ["aba"],
                ["12321"],
                ["Never odd or even"]
            ],
            "hidden": [False, False, False, True, True, False, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])