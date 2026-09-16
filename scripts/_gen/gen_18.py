"""Данные блока 18: Поиск в глубину (DFS)."""
from genlib import run

LECTURE_SLUG = "18_dfs"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "18",
        "slug": "dfs",
        "title": "Поиск в глубину (DFS)",
        "description": "DFS углубляется в граф/сетку, пока возможно, затем откатывается. Разбираем подсчёт островов, максимальную площадь острова и обнаружение циклов (порядок курсов).",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "DFS", "Graphs", "Recursion"],
        "learningOutcomes": [
            "Реализовывать DFS с рекурсией и явным стеком",
            "Применять DFS «затопления» для обхода связных компонент",
            "Обнаруживать циклы через трёхцветную раскраску состояний"
        ],
        "complexity": {
            "timeComplexity": "O(V + E)",
            "spaceComplexity": "O(V)",
            "explanation": "Каждая вершина/клетка обрабатывается один раз; рекурсия хранит стек вызовов глубиной до V."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Чем DFS отличается от BFS при обходе одного графа?",
                "options": [
                    {"id": "opt1", "text": "DFS идёт вглубь, пока не упрётся, затем откатывается", "isCorrect": True, "explanation": "Стек вместо очереди — порядок обхода по глубине."},
                    {"id": "opt2", "text": "DFS работает только на деревьях", "isCorrect": False, "explanation": "DFS применим и к графам."},
                    {"id": "opt3", "text": "DFS всегда даёт кратчайший путь", "isCorrect": False, "explanation": "Кратчайший путь даёт BFS, не DFS."}
                ],
                "hint": "Какой порядок обработки соседей у DFS?"
            },
            {
                "id": "q2",
                "question": "Как найти цикл в ориентированном графе через DFS?",
                "options": [
                    {"id": "opt1", "text": "Пометки «в обходе» и «обработан»; обратное ребро в «в обходе» = цикл", "isCorrect": True, "explanation": "Три состояния 0/1/2 позволяют поймать цикл."},
                    {"id": "opt2", "text": "Подсчётом чисел в узлах", "isCorrect": False, "explanation": "Нумерация цикл не выявляет."},
                    {"id": "opt3", "text": "Сортировкой рёбер по длине", "isCorrect": False, "explanation": "Длина рёбер здесь ни при чём."}
                ],
                "hint": "Какие состояния нужны для детекции цикла?"
            }
        ],
        "attachedTasks": [
            {"taskId": "18-p1", "title": "Острова", "difficulty": "easy", "slug": "number-of-islands"},
            {"taskId": "18-p2", "title": "Максимальная площадь", "difficulty": "medium", "slug": "max-area-of-island"},
            {"taskId": "18-p3", "title": "Курс", "difficulty": "hard", "slug": "course-schedule"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "DFS: стек (рекурсия или явный), помечаем посещённое при добавлении.",
                "Для сетки используйте 4 направления и проверку границ.",
                "Острова: при встрече 1 — увеличить счётчик и «затопить» компоненту.",
                "Площадь: считайте клетки в одном DFS-обходе.",
                "Цикл: состояния 0/1/2, обратное ребро в состояние 1 означает цикл."
            ]
        }
    },
    "problems": [
{
            "id": "18-p1", "title": "Острова", "difficulty": "easy",
            "lecture_id": "18", "order": 1, "entry_function": "num_islands",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def num_islands(grid: list[list[int]]) -> int:\n    \"\"\"Число островов (связных групп единиц) в сетке.\"\"\"\n    ...",
            "description": "Дана сетка `grid` из `0` (вода) и `1` (суша). Остров — связная группа единиц (по 4 направлениям). Верните **количество островов**.\n\n**Функция решения:**\n\n```python\ndef num_islands(grid: list[list[int]]) -> int:\n    ...\n```",
            "examples": [
                {"input": "grid = [[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]", "output": "3", "explanation": "Три отдельных острова."},
                {"input": "grid = [[1]]", "output": "1", "explanation": "Один остров из одной клетки."},
                {"input": "grid = []", "output": "0", "explanation": "Пустая сетка."}
            ],
            "constraints": ["1 ≤ len(grid), len(grid[0]) ≤ 300", "Значения 0 и 1"],
            "hints": [
                "При встрече 1 увеличьте счётчик и «затопите» всю компоненту DFS.",
                "Помечайте клетку посещённой, обнуляя её."
            ],
            "args": [
                [[]],
                [[0, 0], [0, 0]],
                [[1]],
                [[1, 1, 1, 1, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 0], [0, 0, 0, 0, 0]],
                [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1]],
                [[0]],
                [[1, 0, 1]]
            ],
            "wrap_single": True,
            "hidden": [True, True, False, True, False, True, True]
        },
        {
            "id": "18-p2", "title": "Максимальная площадь", "difficulty": "medium",
            "lecture_id": "18", "order": 2, "entry_function": "max_area_of_island",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def max_area_of_island(grid: list[list[int]]) -> int:\n    \"\"\"Максимальная площадь острова (0, если суши нет).\"\"\"\n    ...",
            "description": "Дана сетка `grid` из `0` (вода) и `1` (суша). Верните **максимальную площадь** острова (число клеток) или `0`, если суши нет.\n\n**Функция решения:**\n\n```python\ndef max_area_of_island(grid: list[list[int]]) -> int:\n    ...\n```",
            "examples": [
                {"input": "grid = [[1,1],[1,1]]", "output": "4", "explanation": "Все 4 клетки — один остров."},
                {"input": "grid = [[1,0,1],[0,0,0],[1,0,1]]", "output": "1", "explanation": "Каждый остров из одной клетки."},
                {"input": "grid = [[0]]", "output": "0", "explanation": "Суши нет."}
            ],
            "constraints": ["1 ≤ len(grid), len(grid[0]) ≤ 50", "Значения 0 и 1"],
            "hints": [
                "DFS-площадь каждой компоненты, сохраняйте максимум.",
                "Обнуляйте посещённые клетки."
            ],
            "args": [
                [[]],
                [[0]],
                [[1, 1], [1, 1]],
                [[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]],
                [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
                [[1]],
                [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
            ],
            "wrap_single": True,
            "hidden": [True, False, False, True, True, False, True, True]
        },
        {
            "id": "18-p3", "title": "Курс", "difficulty": "hard",
            "lecture_id": "18", "order": 3, "entry_function": "can_finish",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    \"\"\"Можно ли пройти все курсы без цикла в зависимостях.\"\"\"\n    ...",
            "description": "Дано `num_courses` курсов и список зависимостей `prerequisites` (пары `[a, b]` означают: чтобы пройти `a`, нужно сначала пройти `b`). Верните `True`, если **все курсы можно пройти** (в графе нет цикла).\n\n**Функция решения:**\n\n```python\ndef can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:\n    ...\n```",
            "examples": [
                {"input": "num_courses=2, prerequisites=[[1,0]]", "output": "True", "explanation": "Сначала курс 0, потом 1."},
                {"input": "num_courses=2, prerequisites=[[1,0],[0,1]]", "output": "False", "explanation": "Цикл: 0 зависит от 1 и наоборот."},
                {"input": "num_courses=3, prerequisites=[]", "output": "True", "explanation": "Нет зависимостей — всё проходимо."}
            ],
            "constraints": ["1 ≤ num_courses ≤ 10^4", "0 ≤ len(prerequisites) ≤ 10^5", "Пары [a, b] со значениями в [0, num_courses)"],
            "hints": [
                "Стройте граф: b → a (пререквизит к курсу).",
                "DFS с состояниями 0/1/2; ребро в состояние 1 — цикл."
            ],
            "args": [
                [2, [[1, 0]]],
                [2, [[1, 0], [0, 1]]],
                [1, [[0, 0]]],
                [3, []],
                [0, []],
                [4, [[1, 0], [2, 0], [3, 1], [3, 2]]],
                [3, [[0, 1], [1, 2], [2, 0]]]
            ],
            "hidden": [False, False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])