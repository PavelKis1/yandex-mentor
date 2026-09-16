"""Данные блока 24: Работа со строками."""
from genlib import run

LECTURE_SLUG = "24_strings"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "24",
        "slug": "strings",
        "title": "Строки и хэш-подсчёты",
        "description": "Строковые задачи часто сводятся к подсчёту символов и скользящему окну. Разбираем проверку анаграммы, группировку анаграмм по ключу и длиннейшую подстроку без повторов.",
        "durationMinutes": 12,
        "difficulty": "middle",
        "tags": ["Strings", "Hash Map", "Sliding Window"],
        "learningOutcomes": [
            "Сравнивать анаграммы через подсчёт символов или сортировку",
            "Группировать по ключу, полученному из отсортированной строки",
            "Искать длиннейшую подстроку без повторов методом скользящего окна"
        ],
        "complexity": {
            "timeComplexity": "O(n · k log k)",
            "spaceComplexity": "O(n)",
            "explanation": "Для анаграмм сортируем каждую строку; для длиннейшей подстроки — один проход с двумя индексами."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой ключ использовать для группировки анаграмм?",
                "options": [
                    {"id": "opt1", "text": "Отсортированную строку", "isCorrect": True, "explanation": "Анаграммы дают одинаковую отсортированную строку."},
                    {"id": "opt2", "text": "Длину строки", "isCorrect": False, "explanation": "Строки одной длины не обязаны быть анаграммами."},
                    {"id": "opt3", "text": "Первый символ", "isCorrect": False, "explanation": "Первый символ не объединяет анаграммы."}
                ],
                "hint": "Что общего у анаграмм в отсортированном виде?"
            },
            {
                "id": "q2",
                "question": "Как продвигается левая граница в макс. подстроке без повторов?",
                "options": [
                    {"id": "opt1", "text": "left = позиция повторившегося символа + 1", "isCorrect": True, "explanation": "Перепрыгиваем повторившийся символ, не теряя окно."},
                    {"id": "opt2", "text": "left = 0 всегда", "isCorrect": False, "explanation": "Это сбросило бы окно."},
                    {"id": "opt3", "text": "left = i", "isCorrect": False, "explanation": "Приводит к потере ответа."}
                ],
                "hint": "Что делать, когда текущий символ уже был в окне?"
            }
        ],
        "attachedTasks": [
            {"taskId": "24-p1", "title": "Анаграмма", "difficulty": "easy", "slug": "valid-anagram"},
            {"taskId": "24-p2", "title": "Группировка анаграмм", "difficulty": "medium", "slug": "group-anagrams"},
            {"taskId": "24-p3", "title": "Подстрока", "difficulty": "hard", "slug": "longest-substring-without-repeating"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Анаграммы: одинаковые счётчики букв -> sorted(s).",
                "Ключ группы = ''.join(sorted(s)).",
                "Подстрока без повторов: окно [left, i], словарь последних позиций.",
                "При повторе left = last+1, обновляем best = max(best, i-left+1)."
            ]
        }
    },
    "problems": [
{
            "id": "24-p1", "title": "Анаграмма", "difficulty": "easy",
            "lecture_id": "24", "order": 1, "entry_function": "is_anagram",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def is_anagram(s: str, t: str) -> bool:\n    \"\"\"True, если t — анаграмма s.\"\"\"\n    ...",
            "description": "Даны строки `s` и `t`. Верните `True`, если `t` — **анаграмма** `s`, то есть составлена из тех же символов с той же кратностью.\n\n**Функция решения:**\n\n```python\ndef is_anagram(s: str, t: str) -> bool:\n    ...\n```",
            "examples": [
                {"input": "s = 'anagram', t = 'nagaram'", "output": "True", "explanation": "Один и тот же набор букв."},
                {"input": "s = 'rat', t = 'car'", "output": "False", "explanation": "Разные буквы."},
                {"input": "s = '', t = ''", "output": "True", "explanation": "Обе пустые."}
            ],
            "constraints": ["0 ≤ len(s), len(t) ≤ 5·10^4", "Только строчные латинские буквы"],
            "hints": [
                "Сравните счётчики символов (Counter).",
                "Либо отсортируйте и сравните строки.",
                "Если длины разные — сразу False."
            ],
            "args": [
                ["anagram", "nagaram"],
                ["rat", "car"],
                ["", ""],
                ["ab", "ba"],
                ["a", "b"]
            ],
            "hidden": [False, False, True, True, True]
        },
# P1END
{
            "id": "24-p2", "title": "Группировка анаграмм", "difficulty": "medium",
            "lecture_id": "24", "order": 2, "entry_function": "group_anagrams",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def group_anagrams(strs: list[str]) -> list[list[str]]:\n    \"\"\"Сгруппировать анаграммы вместе.\"\"\"\n    ...",
            "description": "Дан массив строк `strs`. Сгруппируйте анаграммы вместе. Две строки — анаграммы, если составлены из одинаковых букв (с учётом кратности). Верните список групп **в порядке первой встречи ключа**.\n\n**Функция решения:**\n\n```python\ndef group_anagrams(strs: list[str]) -> list[list[str]]:\n    ...\n```",
            "examples": [
                {"input": "strs = ['eat','tea','tan','ate','nat','bat']", "output": "[['eat','tea','ate'],['tan','nat'],['bat']]", "explanation": "Три группы анаграмм."},
                {"input": "strs = ['']", "output": "[['']]", "explanation": "Пустая строка — сама по себе группа."},
                {"input": "strs = ['a']", "output": "[['a']]", "explanation": "Одна группа."}
            ],
            "constraints": ["1 ≤ len(strs) ≤ 10^4", "0 ≤ len(слово) ≤ 100", "Строчные латинские буквы"],
            "hints": [
                "Ключ группы — отсортированный вариант строки.",
                "Складывайте строки в dict: ключ -> список.",
                "Отдавайте значения dict в порядке вставки."
            ],
            "args": [
                ["eat", "tea", "tan", "ate", "nat", "bat"],
                [""],
                ["a"],
                ["a", "b"],
                ["ab", "ba", "abc"]
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True, True]
        },
# P2END
{
            "id": "24-p3", "title": "Подстрока", "difficulty": "hard",
            "lecture_id": "24", "order": 3, "entry_function": "length_of_longest_substring",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def length_of_longest_substring(s: str) -> int:\n    \"\"\"Длина длиннейшей подстроки без повторяющихся символов.\"\"\"\n    ...",
            "description": "Дана строка `s`. Найдите **длину наибольшей подстроки без повторяющихся символов**.\n\n**Функция решения:**\n\n```python\ndef length_of_longest_substring(s: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "s = 'abcabcbb'", "output": "3", "explanation": "Подстрока 'abc' — длина 3."},
                {"input": "s = 'bbbbb'", "output": "1", "explanation": "Все символы одинаковые."},
                {"input": "s = 'pwwkew'", "output": "3", "explanation": "'wke' или 'kew' — длина 3."}
            ],
            "constraints": ["0 ≤ len(s) ≤ 5·10^4", "Символы — ASCII"],
            "hints": [
                "Держите словарь последних позиций символов.",
                "Левую границу окна сдвигайте за прошлый повтор.",
                "best = max(best, i - left + 1) на каждом шаге."
            ],
            "args": [
                "abcabcbb",
                "bbbbb",
                "pwwkew",
                "",
                " ",
                "au"
            ],
            "wrap_single": True,
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])
# EOF