"""Данные блока 15: Динамическое программирование по строкам."""
from genlib import run

LECTURE_SLUG = "15_dp_strings"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "15",
        "slug": "dp-strings",
        "title": "Динамическое программирование по строкам (String DP)",
        "description": "Задачи на подстроки и разбиение строк сводятся к DP, где состояние — позиция в строке. Разбираем поиск наибольшей палиндромной подстроки, разбиение на слова (Word Break) и расстояние редактирования.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "Dynamic Programming", "Strings"],
        "learningOutcomes": [
            "Моделировать подстроки через два индекса-состояния",
            "Строить DP по префиксам для проверки разбиения на слова",
            "Выбирать между алгоритмами центр-расширение и таблицей DP"
        ],
        "complexity": {
            "timeComplexity": "O(n^2)",
            "spaceComplexity": "O(n) / O(n^2)",
            "explanation": "Палиндромная подстрока решается за O(n^2) расширением от центра; Word Break — за O(n^2) с памятью O(n)."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Почему для палиндрома удобен подход «расширение от центра»?",
                "options": [
                    {"id": "opt1", "text": "2n-1 центров и линейное расширение дают O(n^2)", "isCorrect": True, "explanation": "Каждый центр расширяется до O(n) — суммарно O(n^2)."},
                    {"id": "opt2", "text": "Он даёт O(n log n)", "isCorrect": False, "explanation": "Без сложного алгоритма (Манчера) так не выйдет."},
                    {"id": "opt3", "text": "Он не требует перебора центров", "isCorrect": False, "explanation": "Как раз требуется рассмотреть все центры."}
                ],
                "hint": "Сколько точек-центров бывает у строки?"
            },
            {
                "id": "q2",
                "question": "Что означает утверждение dp[i] = True в Word Break?",
                "options": [
                    {"id": "opt1", "text": "Префикс s[:i] можно разбить на слова из словаря", "isCorrect": True, "explanation": "Состояние по префиксу — ключевая идея."},
                    {"id": "opt2", "text": "Вся строка равна слову", "isCorrect": False, "explanation": "Это лишь частный случай."},
                    {"id": "opt3", "text": "Символ s[i] есть в словаре", "isCorrect": False, "explanation": "Речь о разбиении префикса, а не о символе."}
                ],
                "hint": "Что кодирует индекс состояния в этой задаче?"
            }
        ],
        "attachedTasks": [
            {"taskId": "15-p1", "title": "Палиндром", "difficulty": "easy", "slug": "longest-palindromic-substring"},
            {"taskId": "15-p2", "title": "Word Break", "difficulty": "medium", "slug": "word-break"},
            {"taskId": "15-p3", "title": "Расстояние Левенштейна", "difficulty": "hard", "slug": "edit-distance-2"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Для строк используйте позицию (i, j) как состояние.",
                "Палиндром: расширяйтесь от каждого символа и каждой границы.",
                "Word Break: dp[i] = True, если есть разбиение префикса на слова.",
                "Расстояние редактирования: dp[i][j] = 1 + min(вставка/удаление/замена).",
                "Не забывайте обрабатывать пустую строку и один символ."
            ]
        }
    },
    "problems": [
{
            "id": "15-p1", "title": "Палиндром", "difficulty": "easy",
            "lecture_id": "15", "order": 1, "entry_function": "longest_palindrome",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def longest_palindrome(s: str) -> str:\n    \"\"\"Наибольшая палиндромная подстрока (расширение от центра).\"\"\"\n    ...",
            "description": "Дана строка `s`. Верните **наибольшую палиндромную подстроку**. Если палиндромов равной длины несколько — верните первый найденный. Для пустой строки верните пустую строку.\n\n**Функция решения:**\n\n```python\ndef longest_palindrome(s: str) -> str:\n    ...\n```",
            "examples": [
                {"input": "s = 'cbbd'", "output": "'bb'", "explanation": "Наибольший палиндром — 'bb'."},
                {"input": "s = 'babad'", "output": "'aba'", "explanation": "'aba' — палиндром длины 3 ('bab' тоже подходит)."},
                {"input": "s = 'a'", "output": "'a'", "explanation": "Один символ всегда палиндром."}
            ],
            "constraints": ["0 ≤ len(s) ≤ 1000", "Строка из строчных латинских букв"],
            "hints": [
                "Берите каждый символ и каждую границу как центр.",
                "Расширяйте центр, пока края равны; запоминайте самый длинный результат."
            ],
            "args": [["cbbd"], [""], ["a"], ["babad"], ["aaabaaa"], ["forgeeksskeegfor"], ["abc"], ["racecar"]],
            "hidden": [False, False, True, False, True, True, True, True]
        },
        {
            "id": "15-p2", "title": "Word Break", "difficulty": "medium",
            "lecture_id": "15", "order": 2, "entry_function": "word_break",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def word_break(s: str, word_dict: list[str]) -> bool:\n    \"\"\"Можно ли разбить строку на слова из словаря (слова можно повторять).\"\"\"\n    ...",
            "description": "Дана строка `s` и словарь `word_dict`. Верните `True`, если `s` можно **разбить на последовательность слов** из словаря (каждое слово можно использовать неограниченно).\n\n**Функция решения:**\n\n```python\ndef word_break(s: str, word_dict: list[str]) -> bool:\n    ...\n```",
            "examples": [
                {"input": "s = 'leetcode', word_dict = ['leet', 'code']", "output": "True", "explanation": "'leet' + 'code'."},
                {"input": "s = 'catsandog', word_dict = ['cats','dog','sand','and','cat']", "output": "False", "explanation": "Ни одно разбиение не покрывает всю строку."},
                {"input": "s = '', word_dict = []", "output": "True", "explanation": "Пустая строка тривиально разбивается."}
            ],
            "constraints": ["0 ≤ len(s) ≤ 300", "0 ≤ len(word_dict) ≤ 1000", "Слово — непустая строка из строчных букв"],
            "hints": [
                "dp[i] = True, если префикс s[:i] разбивается на слова.",
                "Проверяйте все разбиения: s[j:i] ∈ словаря и dp[j] == True."
            ],
            "args": [["leetcode", ["leet", "code"]], ["applepenapple", ["apple", "pen"]], ["catsandog", ["cats", "dog", "sand", "and", "cat"]], ["", []], ["aaaa", ["a"]], ["aaaa", ["aaa", "aa"]], ["bb", []], ["cars", ["car", "ca", "rs"]]],
            "hidden": [False, False, False, True, True, True, True, True]
        },
        {
            "id": "15-p3", "title": "Расстояние Левенштейна", "difficulty": "hard",
            "lecture_id": "15", "order": 3, "entry_function": "edit_distance",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def edit_distance(s1: str, s2: str) -> int:\n    \"\"\"Минимальное число операций вставки/удаления/замены.\"\"\"\n    ...",
            "description": "Даны строки `s1` и `s2`. За одну операцию можно **вставить**, **удалить** или **заменить** символ. Верните **минимальное расстояние** (число операций) для превращения `s1` в `s2`.\n\n**Функция решения:**\n\n```python\ndef edit_distance(s1: str, s2: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "s1 = 'kitten', s2 = 'sitting'", "output": "3", "explanation": "Замена k→s, вставка g, замена e→i."},
                {"input": "s1 = '', s2 = 'abc'", "output": "3", "explanation": "Три вставки."},
                {"input": "s1 = '', s2 = ''", "output": "0", "explanation": "Строки уже равны."}
            ],
            "constraints": ["0 ≤ len(s1), len(s2) ≤ 500", "Строки из строчных латинских букв"],
            "hints": [
                "dp[i][j] = dp[i-1][j-1], если символы равны.",
                "Иначе 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]).",
                "Оптимизируйте память до одной строки dp."
            ],
            "args": [["horse", "ros"], ["intention", "execution"], ["", ""], ["a", ""], ["kitten", "sitting"], ["flaw", "lawn"]],
            "hidden": [True, True, True, False, False, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])