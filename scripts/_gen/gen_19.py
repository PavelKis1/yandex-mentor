"""Данные блока 19: Топологическая сортировка."""
from genlib import run

LECTURE_SLUG = "19_toposort"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "19",
        "slug": "toposort",
        "title": "Топологическая сортировка (Topological Sort)",
        "description": "Топосорт упорядочивает вершины ориентированного ациклического графа так, что все рёбра идут в одну сторону. Разбираем алгоритм Кана, обнаружение циклов и восстановление порядка из словаря.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "Graphs", "Topological Sort", "DAG"],
        "learningOutcomes": [
            "Реализовывать топологическую сортировку алгоритмом Кана",
            "Определять наличие цикла по некорректному результату топосорта",
            "Применять топосорт к восстановлению порядка в задаче со словарём"
        ],
        "complexity": {
            "timeComplexity": "O(V + E)",
            "spaceComplexity": "O(V)",
            "explanation": "Каждое ребро разбирается один раз в алгоритме Кана; память — очередь и степени вершин."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой граф можно отсортировать топологически?",
                "options": [
                    {"id": "opt1", "text": "Ориентированный ациклический граф (DAG)", "isCorrect": True, "explanation": "Цикл делает топосорт невозможным."},
                    {"id": "opt2", "text": "Любой граф", "isCorrect": False, "explanation": "При цикле нет начального порядка."},
                    {"id": "opt3", "text": "Только полный граф", "isCorrect": False, "explanation": "Полнота не требуется."}
                ],
                "hint": "Какое свойство графа исключает топосорт?"
            },
            {
                "id": "q2",
                "question": "Суть алгоритма Кана (Kahn)?",
                "options": [
                    {"id": "opt1", "text": "Брать вершины с нулевой входящей степенью и удалять их рёбра", "isCorrect": True, "explanation": "Так и получается корректный порядок."},
                    {"id": "opt2", "text": "Случайный обход соседей", "isCorrect": False, "explanation": "Случайный обход не гарантирует порядок."},
                    {"id": "opt3", "text": "Подсчитывать исходящие рёбра", "isCorrect": False, "explanation": "Нужны входящие степени, не исходящие."}
                ],
                "hint": "Какую метрику вершин использует Каhн?"
            }
        ],
        "attachedTasks": [
            {"taskId": "19-p1", "title": "Сортировка курсов", "difficulty": "easy", "slug": "course-order"},
            {"taskId": "19-p2", "title": "Проверка цикла", "difficulty": "medium", "slug": "graph-cycle"},
            {"taskId": "19-p3", "title": "Словарь инопланетян", "difficulty": "hard", "slug": "alien-dictionary"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Топосорт возможен только в DAG.",
                "Kahn: очередь вершин со степенью 0, снимаем рёбра, уменьшаем степени.",
                "Если порядок короче, чем вершин — в графе цикл.",
                "Словарный порядок: рёбра из соседних слов по первому различию.",
                "Обрабатывайте конфликт префиксов (длинное слово раньше короткого) как ошибку."
            ]
        }
    },
    "problems": [
{
            "id": "19-p1", "title": "Сортировка курсов", "difficulty": "easy",
            "lecture_id": "19", "order": 1, "entry_function": "topological_sort",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def topological_sort(graph: dict[int, list[int]], n: int) -> list[int]:\n    \"\"\"Топологический порядок вершин ([] при цикле).\"\"\"\n    ...",
            "description": "Дан ориентированный граф `graph: {vertex: [соседи]}` с вершинами `0..n-1`. Верните **топологический порядок** вершин: каждое ребро `u -> v` означает, что `u` идёт раньше `v`. Если граф содержит цикл — верните `[]`.\n\n**Функция решения:**\n\n```python\ndef topological_sort(graph: dict[int, list[int]], n: int) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "graph={0:[1],1:[2],2:[]}, n=3", "output": "[0, 1, 2]", "explanation": "Цепочка зависимостей."},
                {"input": "graph={}, n=3", "output": "[0, 1, 2]", "explanation": "Изолированные вершины в порядке номеров."},
                {"input": "graph={0:[1],1:[0],2:[]}, n=3", "output": "[]", "explanation": "Цикл 0↔1."}
            ],
            "constraints": ["0 ≤ n ≤ 10^4", "0 ≤ E ≤ 10^5", "Вершины в диапазоне [0, n)"],
            "hints": [
                "Посчитайте входящие степени всех вершин.",
                "Очередь из вершин со степенью 0; снимая ребро, уменьшайте степень соседа.",
                "Если собрано меньше n вершин — в графе цикл."
            ],
            "args": [
                [{"0": [1], "1": [2], "2": []}, 3],
                [{"0": [1], "1": [0], "2": []}, 3],
                [{}, 3],
                [{"0": [1], "2": [1]}, 3],
                [{"0": [1, 2], "1": [3], "2": [3], "3": []}, 4]
            ],
            "hidden": [False, True, False, True, True]
        },
        {
            "id": "19-p2", "title": "Проверка цикла", "difficulty": "medium",
            "lecture_id": "19", "order": 2, "entry_function": "has_cycle",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def has_cycle(graph: dict[int, list[int]], n: int) -> bool:\n    \"\"\"Есть ли цикл в ориентированном графе.\"\"\"\n    ...",
            "description": "Дан **ориентированный** граф `graph: {vertex: [соседи]}` с вершинами `0..n-1`. Верните `True`, если в графе есть **цикл**.\n\n**Функция решения:**\n\n```python\ndef has_cycle(graph: dict[int, list[int]], n: int) -> bool:\n    ...\n```",
            "examples": [
                {"input": "graph={0:[1],1:[0],2:[]}, n=3", "output": "True", "explanation": "Цикл между 0 и 1."},
                {"input": "graph={}, n=3", "output": "False", "explanation": "Рёбер нет."},
                {"input": "graph={0:[0]}, n=1", "output": "True", "explanation": "Самопетля — цикл."}
            ],
            "constraints": ["0 ≤ n ≤ 10^4", "0 ≤ E ≤ 10^5"],
            "hints": [
                "DFS с состояниями 0 (не посещён), 1 (в обходе), 2 (готов).",
                "Ребро в вершину со статусом 1 — цикл."
            ],
            "args": [
                [{"0": [1], "1": [0], "2": []}, 3],
                [{}, 3],
                [{"0": [0]}, 1],
                [{"0": [1], "1": [2]}, 3],
                [{"0": [1], "1": [2], "2": [0]}, 3],
                [{"0": [1]}, 2]
            ],
            "hidden": [False, True, False, True, True, True]
        },
        {
            "id": "19-p3", "title": "Словарь инопланетян", "difficulty": "hard",
            "lecture_id": "19", "order": 3, "entry_function": "alien_order",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def alien_order(words: list[str]) -> str:\n    \"\"\"Порядок букв в словаре; '' при противоречии/цикле.\"\"\"\n    ...",
            "description": "Слова `words` отсортированы в лексикографическом порядке **неизвестного алфавита**. Верните **строку-порядок букв** этого алфавита. Если порядок восстановить нельзя (цикл или конфликт префиксов) — верните пустую строку `''`.\n\n**Функция решения:**\n\n```python\ndef alien_order(words: list[str]) -> str:\n    ...\n```",
            "examples": [
                {"input": "words = ['wrt','wrf','er','ett','rftt']", "output": "'wertf'", "explanation": "Порядок, восстановленный по первым различиям пар."},
                {"input": "words = ['z','x']", "output": "'zx'", "explanation": "z идёт раньше x."},
                {"input": "words = ['abc','ab']", "output": "''", "explanation": "Конфликт префиксов: 'ab' меньше, но длиннее — некорректно."}
            ],
            "constraints": ["0 ≤ len(words) ≤ 100", "Слова из строчных латинских букв"],
            "hints": [
                "Сравните соседние слова: первое различие даёт ребро x→y.",
                "Префикс-конфликт: длинное слово раньше короткого — ответ пустой.",
                "Примените топосорт (Kahn) по буквам; при цикле верните ''."
            ],
            "args": [
                [["wrt", "wrf", "er", "ett", "rftt"]],
                [["z", "x"]],
                [["a"]],
                [[]],
                [["abc", "ab"]],
                [["z", "x", "z"]],
                [["ab", "adc"]],
                [["abcd"]]
            ],
            "hidden": [False, True, False, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])