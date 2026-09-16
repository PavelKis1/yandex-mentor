"""Данные блока 20: Система непересекающихся множеств (DSU)."""
from genlib import run

LECTURE_SLUG = "20_union_find"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "20",
        "slug": "union-find",
        "title": "Система непересекающихся множеств (Union-Find / DSU)",
        "description": "DSU объединяет множества и отвечает на вопрос «в одной ли компоненте». Работает почти за O(1) благодаря сжатию путей. Разбираем число провинций, лишнее ребро и слияние аккаунтов.",
        "durationMinutes": 15,
        "difficulty": "middle",
        "tags": ["Algorithms", "Graphs", "Union-Find", "DSU"],
        "learningOutcomes": [
            "Реализовывать find (со сжатием путей) и union",
            "Считать компоненты связности и находить ребро-цикл",
            "Применять DSU для группировки по общему ключу"
        ],
        "complexity": {
            "timeComplexity": "O(α(n)) на операцию",
            "spaceComplexity": "O(n)",
            "explanation": "Со сжатием путей и union по весу операции почти константны (обратная функция Аккермана)."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что даёт сжатие путей (path compression)?",
                "options": [
                    {"id": "opt1", "text": "find становится почти O(1) в среднем", "isCorrect": True, "explanation": "Родителя узла напрямую ставим в корень."},
                    {"id": "opt2", "text": "Гарантирует сортировку вершин", "isCorrect": False, "explanation": "Сортировка не связана с DSU."},
                    {"id": "opt3", "text": "Добавляет рёбра в граф", "isCorrect": False, "explanation": "DSU не строит рёбра."}
                ],
                "hint": "Какой эффект от перенаправления узлов к корню?"
            },
            {
                "id": "q2",
                "question": "Когда union находит лишнее ребро в графе?",
                "options": [
                    {"id": "opt1", "text": "Когда обе вершины уже в одной компоненте", "isCorrect": True, "explanation": "Ребро замыкает цикл внутри одной компоненты."},
                    {"id": "opt2", "text": "Когда вершины в разных компонентах", "isCorrect": False, "explanation": "Тогда ребро просто соединяет два множества."},
                    {"id": "opt3", "text": "Когда рёбер больше 100", "isCorrect": False, "explanation": "Число рёбер ни при чём."}
                ],
                "hint": "Какой результат union указывает на цикл?"
            }
        ],
        "attachedTasks": [
            {"taskId": "20-p1", "title": "Провинции", "difficulty": "easy", "slug": "number-of-provinces"},
            {"taskId": "20-p2", "title": "Лишнее ребро", "difficulty": "medium", "slug": "redundant-connection"},
            {"taskId": "20-p3", "title": "Слияние аккаунтов", "difficulty": "hard", "slug": "accounts-merge"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "parent[i] указывает на родителя; find — к корню со сжатием путей.",
                "union(a,b): находим корни; если равны — уже в одной компоненте.",
                "Число компонент = число различных find(i).",
                "Лишнее ребро: union двух узлов одной компоненты.",
                "DSU по ключу (email) объединяет записи с общим значением."
            ]
        }
    },
    "problems": [
{
            "id": "20-p1", "title": "Провинции", "difficulty": "easy",
            "lecture_id": "20", "order": 1, "entry_function": "find_circle_num",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def find_circle_num(is_connected: list[list[int]]) -> int:\n    \"\"\"Число провинций (компонент связности) по матрице смежности.\"\"\"\n    ...",
            "description": "Дана матрица смежности `is_connected` размером `n x n`: `is_connected[i][j] == 1`, если города `i` и `j` соединены напрямую. **Провинция** — группа прямо или косвенно связанных городов. Верните **количество провинций**.\n\n**Функция решения:**\n\n```python\ndef find_circle_num(is_connected: list[list[int]]) -> int:\n    ...\n```",
            "examples": [
                {"input": "is_connected = [[1,1,0],[1,1,0],[0,0,1]]", "output": "2", "explanation": "Города 0-1 связаны, город 2 отдельно."},
                {"input": "is_connected = [[1]]", "output": "1", "explanation": "Один город — одна провинция."},
                {"input": "is_connected = []", "output": "0", "explanation": "Пустая матрица."}
            ],
            "constraints": ["0 ≤ n ≤ 200", "is_connected[i][i] = 1", "Матрица симметрична"],
            "hints": [
                "Union все пары с is_connected[i][j] == 1.",
                "Ответ — число различных корней find(i)."
            ],
            "args": [
                [[1, 1, 0], [1, 1, 0], [0, 0, 1]],
                [[1]],
                [],
                [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
                [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
            ],
            "wrap_single": True,
            "hidden": [False, True, True, True, True, True]
        },
        {
            "id": "20-p2", "title": "Лишнее ребро", "difficulty": "medium",
            "lecture_id": "20", "order": 2, "entry_function": "find_redundant_connection",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def find_redundant_connection(edges: list[list[int]]) -> list[int]:\n    \"\"\"Первое ребро, замыкающее цикл ([] — цикла нет).\"\"\"\n    ...",
            "description": "Дан список `edges` (рёбра **неориентированного** графа; вершины 1..n). Граф начался как дерево, но при добавлении одного ребра появился цикл. Верните это **лишнее ребро** (первое, замыкающее цикл). Если цикла нет — верните `[]`.\n\n**Функция решения:**\n\n```python\ndef find_redundant_connection(edges: list[list[int]]) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "edges = [[1,2],[1,3],[2,3]]", "output": "[2, 3]", "explanation": "Ребро [2,3] замыкает цикл 1-2-3-1."},
                {"input": "edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]", "output": "[1, 4]", "explanation": "[1,4] создаёт цикл 1-2-3-4-1."},
                {"input": "edges = [[1,2]]", "output": "[]", "explanation": "Цикла нет."}
            ],
            "constraints": ["0 ≤ len(edges) ≤ 1000", "Рёбра [u, v] с u, v ≥ 1"],
            "hints": [
                "Пройдите рёбра по порядку, вызывая union.",
                "Если обе вершины уже в одной компоненте — это лишнее ребро."
            ],
            "args": [
                [[1, 2], [1, 3], [2, 3]],
                [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],
                [],
                [[1, 2], [2, 3], [1, 3]],
                [[1, 2]]
            ],
            "wrap_single": True,
            "hidden": [False, False, True, True, True]
        },
        {
            "id": "20-p3", "title": "Слияние аккаунтов", "difficulty": "hard",
            "lecture_id": "20", "order": 3, "entry_function": "accounts_merge",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:\n    \"\"\"Объединить аккаунты с общими email: [имя] + отсортированные email.\"\"\"\n    ...",
            "description": "Дан список `accounts`, где каждый элемент `[имя, email1, email2, ...]`. Аккаунты одного человека могут повторяться. Объедините аккаунты, у которых есть **общий email**: результат `[имя, email...]` с **отсортированными** email без дубликатов. Порядок аккаунтов в ответе — по возрастанию первого email.\n\n**Функция решения:**\n\n```python\ndef accounts_merge(accounts: list[list[str]]) -> list[list[str]]:\n    ...\n```",
            "examples": [
                {"input": "accounts=[['John','a@','b@'],['John','b@','c@']]", "output": "[['John','a@','b@','c@']]", "explanation": "Общий email 'b@' объединяет оба аккаунта."},
                {"input": "accounts=[['Mary','m@']]", "output": "[['Mary','m@']]", "explanation": "Один аккаунт без слияния."},
                {"input": "accounts=[]", "output": "[]", "explanation": "Пустой список."}
            ],
            "constraints": ["0 ≤ len(accounts) ≤ 1000", "0 ≤ email на аккаунт ≤ 10", "Строки: имя и email"],
            "hints": [
                "Каждому email сопоставьте первого владельца; union по email внутри аккаунта.",
                "Сгруппируйте email по корню и отсортируйте их.",
                "Отсортируйте группы по минимальному email."
            ],
            "args": [
                [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"], ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]],
                [["a", "x@m.co", "y@m.co"], ["a", "y@m.co", "z@m.co"]],
                [["Gabe", "g0@m.co", "g3@m.co", "g1@m.co"], ["Kevin", "k3@m.co", "k5@m.co", "k0@m.co"], ["Hanzo", "h0@m.co", "h1@m.co"]],
                [["Hanzo", "h0@m.co", "h1@m.co"]],
                []
            ],
            "wrap_single": True,
            "hidden": [False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])