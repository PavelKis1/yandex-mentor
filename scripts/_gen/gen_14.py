"""Данные блока 14: Динамическое программирование (2D)."""
from genlib import run

LECTURE_SLUG = "14_dp_2d"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "14",
        "slug": "dp-2d",
        "title": "Динамическое программирование: 2D (DP 2D)",
        "description": "Когда состояние задаётся двумя параметрами (позиции в двух строках, координаты в сетке), строим двумерную таблицу. Разбираем число путей в сетке, наибольшую общую подпоследовательность (LCS) и расстояние редактирования.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "Dynamic Programming", "Strings"],
        "learningOutcomes": [
            "Строить таблицу DP размером O(m*n) по двум параметрам",
            "Выводить переходы для сеточных задач и сравнения строк",
            "Оптимизировать память до двух одномерных строк"
        ],
        "complexity": {
            "timeComplexity": "O(m * n)",
            "spaceComplexity": "O(m * n) → O(n)",
            "explanation": "Заполняем таблицу m×n; для LCS и редакционного расстояния достаточно хранить предыдущую строку."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Когда рекуррентность становится двумерной?",
                "options": [
                    {"id": "opt1", "text": "Когда состояние описывается двумя независимыми параметрами", "isCorrect": True, "explanation": "Два параметра → таблица dp[m][n]."},
                    {"id": "opt2", "text": "Когда данные отсортированы", "isCorrect": False, "explanation": "Сортировка к размерности таблицы отношения не имеет."},
                    {"id": "opt3", "text": "Когда в массиве больше 100 элементов", "isCorrect": False, "explanation": "Размер таблицы зависит от параметров, а не от порога длины."}
                ],
                "hint": "От чего зависит содержимое ячейки dp[i][j]?"
            },
            {
                "id": "q2",
                "question": "Как в LCS обновляется ячейка при совпадении символов?",
                "options": [
                    {"id": "opt1", "text": "dp[i][j] = dp[i-1][j-1] + 1", "isCorrect": True, "explanation": "Продлеваем общую подпоследовательность на один символ."},
                    {"id": "opt2", "text": "dp[i][j] = 0", "isCorrect": False, "explanation": "Так считают длины, а не LCS."},
                    {"id": "opt3", "text": "dp[i][j] = dp[i][j-1]", "isCorrect": False, "explanation": "Это лишь один из вариантов для случая несовпадения."}
                ],
                "hint": "Что даёт совпадение двух символов?"
            }
        ],
        "attachedTasks": [
            {"taskId": "14-p1", "title": "Уникальные пути", "difficulty": "easy", "slug": "unique-paths"},
            {"taskId": "14-p2", "title": "LCS", "difficulty": "medium", "slug": "longest-common-subsequence"},
            {"taskId": "14-p3", "title": "Расстояние редактирования", "difficulty": "hard", "slug": "edit-distance"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Определите обе оси таблицы (индексы строк/колонок или двух строк).",
                "Задайте базу: первую строку и первый столбец.",
                "Переход: сдвиг по i-1/j-1 с учётом равенства символов.",
                "Для сетки: dp[i][j] = dp[i-1][j] + dp[i][j-1] при движении вправо/вниз.",
                "Память снижайте до двух строк, если переходам нужна только предыдущая строка."
            ]
        }
    },
    "problems": [
{
            "id": "14-p1", "title": "Уникальные пути", "difficulty": "easy",
            "lecture_id": "14", "order": 1, "entry_function": "unique_paths",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def unique_paths(m: int, n: int) -> int:\n    \"\"\"Число путей из левого верхнего угла в правый нижний.\"\"\"\n    ...",
            "description": "Есть сетка размером `m x n`. Робот стартует в левом верхнем углу и может двигаться только **вниз** или **вправо**. Верните количество уникальных путей до правого нижнего угла. Если `m < 1` или `n < 1`, верните 0.\n\n**Функция решения:**\n\n```python\ndef unique_paths(m: int, n: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "m = 3, n = 7", "output": "28", "explanation": "Число сочетаний C(3+7-2, 2) = 28."},
                {"input": "m = 3, n = 3", "output": "6", "explanation": "Шесть различных маршрутов."},
                {"input": "m = 0, n = 5", "output": "0", "explanation": "Пустой размер — путей нет."}
            ],
            "constraints": ["0 ≤ m, n ≤ 100", "Движение только вниз и вправо"],
            "hints": [
                "dp[i][j] = dp[i-1][j] + dp[i][j-1].",
                "Можно хранить только одну строку, обновляя её слева направо."
            ],
            "args": [[3, 7], [1, 1], [0, 5], [5, 0], [1, 10], [3, 3], [2, 2], [7, 3]],
            "hidden": [False, False, False, True, True, True, False, True]
        },
        {
            "id": "14-p2", "title": "LCS", "difficulty": "medium",
            "lecture_id": "14", "order": 2, "entry_function": "longest_common_subsequence",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def longest_common_subsequence(s1: str, s2: str) -> int:\n    \"\"\"Длина наибольшей общей подпоследовательности.\"\"\"\n    ...",
            "description": "Даны строки `s1` и `s2`. Верните длину **наибольшей общей подпоследовательности** (символы идут по порядку в обеих строках, но не обязательно подряд).\n\n**Функция решения:**\n\n```python\ndef longest_common_subsequence(s1: str, s2: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "s1 = 'abcde', s2 = 'ace'", "output": "3", "explanation": "Общая подпоследовательность 'ace'."},
                {"input": "s1 = 'abc', s2 = 'def'", "output": "0", "explanation": "Общих символов нет."},
                {"input": "s1 = 'abc', s2 = 'abc'", "output": "3", "explanation": "Строки совпадают полностью."}
            ],
            "constraints": ["0 ≤ len(s1), len(s2) ≤ 1000", "Строки из строчных латинских букв"],
            "hints": [
                "При s1[i-1] == s2[j-1]: dp[i][j] = dp[i-1][j-1] + 1.",
                "Иначе dp[i][j] = max(dp[i-1][j], dp[i][j-1]).",
                "Храните только предыдущую строку dp."
            ],
            "args": [["abcde", "ace"], ["abc", "def"], ["", "abc"], ["abc", "abc"], ["AGGTAB", "GXTXAYB"], ["oxcpqrsvwf", "shmtulqrypy"]],
            "hidden": [False, False, True, False, True, True]
        },
        {
            "id": "14-p3", "title": "Расстояние редактирования", "difficulty": "hard",
            "lecture_id": "14", "order": 3, "entry_function": "edit_distance",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def edit_distance(s1: str, s2: str) -> int:\n    \"\"\"Минимальное число вставок/удалений/замен.\"\"\"\n    ...",
            "description": "Даны строки `s1` и `s2`. За одну операцию можно **вставить**, **удалить** или **заменить** один символ. Верните минимальное количество операций, превращающих `s1` в `s2`.\n\n**Функция решения:**\n\n```python\ndef edit_distance(s1: str, s2: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "s1 = 'horse', s2 = 'ros'", "output": "3", "explanation": "Удалить h, заменить o→r, удалить e."},
                {"input": "s1 = 'intention', s2 = 'execution'", "output": "5", "explanation": "Классический пример из LeetCode."},
                {"input": "s1 = '', s2 = ''", "output": "0", "explanation": "Строки уже равны."}
            ],
            "constraints": ["0 ≤ len(s1), len(s2) ≤ 500", "Строки из строчных латинских букв"],
            "hints": [
                "При равенстве символов переносите значение по диагонали.",
                "Иначе dp[i][j] = 1 + min(вставка, удаление, замена).",
                "Используйте одну строку dp и переменную prev по диагонали."
            ],
            "args": [["horse", "ros"], ["intention", "execution"], ["", ""], ["abc", "abc"], ["a", "b"], ["kitten", "sitting"], ["flaw", "lawn"]],
            "hidden": [False, False, True, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])