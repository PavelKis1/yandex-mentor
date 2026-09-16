"""Данные блока 17: Поиск в ширину (BFS)."""
from genlib import run

LECTURE_SLUG = "17_bfs"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "17",
        "slug": "bfs",
        "title": "Поиск в ширину (BFS)",
        "description": "BFS обходит граф по уровням и находит кратчайший путь в невзвешенном графе. Разбираем открытие кодового замка, распространение гнили по сетке и кратчайший путь в графе.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Algorithms", "BFS", "Graphs", "Queue"],
        "learningOutcomes": [
            "Реализовывать BFS с очередью и массивом посещённых вершин",
            "Применять мультиисточниковый BFS для параллельного распространения",
            "Использовать BFS для поиска кратчайшего пути в невзвешенном графе"
        ],
        "complexity": {
            "timeComplexity": "O(V + E)",
            "spaceComplexity": "O(V)",
            "explanation": "Каждая вершина попадает в очередь один раз; память — очередь и множество посещённых."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Почему BFS даёт кратчайший путь в невзвешенном графе?",
                "options": [
                    {"id": "opt1", "text": "Вершины обрабатываются по уровням удалённости от старта", "isCorrect": True, "explanation": "Первая встреча вершины — по кратчайшему пути."},
                    {"id": "opt2", "text": "BFS перебирает рёбра по весу", "isCorrect": False, "explanation": "В невзвешенном графе вес единичный."},
                    {"id": "opt3", "text": "Он сортирует граф", "isCorrect": False, "explanation": "Сортировка к кратчайшему пути не относится."}
                ],
                "hint": "Как устроен порядок обхода BFS?"
            },
            {
                "id": "q2",
                "question": "Какой структурой данных реализуется BFS?",
                "options": [
                    {"id": "opt1", "text": "Очередь (deque)", "isCorrect": True, "explanation": "Берём спереди, добавляем в конец — FIFO."},
                    {"id": "opt2", "text": "Стек", "isCorrect": False, "explanation": "Стек даёт DFS, а не BFS."},
                    {"id": "opt3", "text": "Куча", "isCorrect": False, "explanation": "Куча нужна для приоритетных обходов."}
                ],
                "hint": "Какой принцип обслуживания (FIFO/LIFO) у BFS?"
            }
        ],
        "attachedTasks": [
            {"taskId": "17-p1", "title": "Открытие замка", "difficulty": "easy", "slug": "open-the-lock"},
            {"taskId": "17-p2", "title": "Гниющие апельсины", "difficulty": "medium", "slug": "rotting-oranges"},
            {"taskId": "17-p3", "title": "Кратчайший путь", "difficulty": "hard", "slug": "shortest-path-bfs"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Используйте deque: popleft() для текущего уровня, append() для соседей.",
                "Отмечайте посещённые вершины, чтобы избежать зацикливания.",
                "Расстояние фиксируйте вместе с вершиной в очереди.",
                "Мультиисточниковый BFS: стартовый слой кладём в очередь целиком.",
                "Первое посещение цели = длина кратчайшего пути. O(V+E)."
            ]
        }
    },
    "problems": [
{
            "id": "17-p1", "title": "Открытие замка", "difficulty": "easy",
            "lecture_id": "17", "order": 1, "entry_function": "open_lock",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def open_lock(deadends: list[str], target: str) -> int:\n    \"\"\"Минимальное число поворотов до target, обходя deadends (-1, если нельзя).\"\"\"\n    ...",
            "description": "Замок с 4 круглыми цифрами (`0000`..`9999`). За один ход любая цифра меняется на +1 или −1 (по кругу). Запрещённые состояния — `deadends`. Верните **минимальное число поворотов** от `0000` до `target` или **-1**, если добраться нельзя. Если `0000` в deadends — сразу `-1`.\n\n**Функция решения:**\n\n```python\ndef open_lock(deadends: list[str], target: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "deadends = ['0201','0101','0102','1212','2002'], target = '0202'", "output": "6", "explanation": "Кратчайший маршрут обходит запреты."},
                {"input": "deadends = ['0000'], target = '8888'", "output": "-1", "explanation": "Старт недоступен сразу."},
                {"input": "deadends = [], target = '0000'", "output": "0", "explanation": "Уже на месте."}
            ],
            "constraints": ["target — строка из 4 цифр", "0 ≤ len(deadends) ≤ 1000", "Состояния — все 10^4 комбинаций"],
            "hints": [
                "Представьте каждое состояние как вершину, поворот — как ребро.",
                "Стартовая очередь из '0000', каждое посещение фиксируйте и не повторяйте.",
                "Меняйте цифру: (d + 1) % 10 и (d - 1) % 10."
            ],
            "args": [
                [["0201", "0101", "0102", "1212", "2002"], "0202"],
                [["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888"],
                [["0000"], "8888"],
                [[], "0202"],
                [[], "0000"],
                [["1000"], "0001"]
            ],
            "hidden": [False, True, False, True, True, True]
        },
        {
            "id": "17-p2", "title": "Гниющие апельсины", "difficulty": "medium",
            "lecture_id": "17", "order": 2, "entry_function": "oranges_rotting",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def oranges_rotting(grid: list[list[int]]) -> int:\n    \"\"\"Минуты до полного гниения (0 — пусто, 1 — свежий, 2 — гнилой).\"\"\"\n    ...",
            "description": "В сетке `grid`: `0` — пусто, `1` — свежий апельсин, `2` — гнилой. Каждую минуту гнилой заражает соседние (вверх/вниз/влево/вправо) свежие. Верните **число минут**, за которые сгниют все свежие, или `0`, если свежих нет, или `-1`, если какие-то свежие недостижимы.\n\n**Функция решения:**\n\n```python\ndef oranges_rotting(grid: list[list[int]]) -> int:\n    ...\n```",
            "examples": [
                {"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4", "explanation": "Все апельсины сгниют за 4 минуты."},
                {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1", "explanation": "Один свежий недостижим."},
                {"input": "grid = [[0,2]]", "output": "0", "explanation": "Свежих нет."}
            ],
            "constraints": ["1 ≤ len(grid), len(grid[0]) ≤ 20", "Значения 0, 1, 2"],
            "hints": [
                "Мультиисточниковый BFS: положите все гнилые в очередь с временем 0.",
                "Заражённые добавляйте в конец с временем t+1.",
                "Считайте свежие; если после BFS они остались — верните -1."
            ],
            "args": [
                [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]],
                [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]],
                [[[0, 2]]],
                [[]],
                [[[2, 2], [2, 2]]],
                [[[1]]],
                [[[0, 2, 1]]],
                [[[2, 1], [1, 0]]]
            ],
            "hidden": [False, False, False, True, True, True, True, True]
        },
        {
            "id": "17-p3", "title": "Кратчайший путь", "difficulty": "hard",
            "lecture_id": "17", "order": 3, "entry_function": "shortest_path",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def shortest_path(graph: dict[int, list[int]], start: int, end: int) -> int:\n    \"\"\"Длина кратчайшего пути в невзвешенном графе или -1.\"\"\"\n    ...",
            "description": "Дан **невзвешенный** граф `graph: {node: [соседи]}`. Верните **минимальное количество рёбер** от `start` до `end`. Если `start == end`, верните `0`; если конца не достичь — верните `-1`.\n\n**Функция решения:**\n\n```python\ndef shortest_path(graph: dict[int, list[int]], start: int, end: int) -> int:\n    ...\n```",
            "examples": [
                {"input": "graph={0:[1,2],1:[2],2:[3],3:[]}, start=0, end=3", "output": "2", "explanation": "Путь 0→2→3 (2 ребра)."},
                {"input": "graph={0:[1],1:[0]}, start=0, end=0", "output": "0", "explanation": "Старт равен концу."},
                {"input": "graph={0:[1]}, start=0, end=5", "output": "-1", "explanation": "Вершина 5 недостижима."}
            ],
            "constraints": ["Вершины графа — целые числа", "0 ≤ E ≤ 10^4", "Граф невзвешенный"],
            "hints": [
                "Очередь хранит (вершина, расстояние).",
                "Соседей из graph.get(node, []) обходите, пропуская посещённые.",
                "Первое попадание в end возвращает расстояние."
            ],
            "args": [
                [{"0": [1, 2], "1": [2], "2": [3], "3": []}, 0, 3],
                [{"0": [1], "1": [0]}, 0, 0],
                [{"0": [1]}, 0, 5],
                [{}, 1, 2],
                [{"1": [2, 3], "2": [4], "3": [4], "4": []}, 1, 4],
                [{"1": [2], "2": [1]}, 1, 2]
            ],
            "hidden": [False, True, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])