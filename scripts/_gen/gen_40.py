"""Данные блока 40: Индексы БД (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "40_indexes"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "40",
        "slug": "indexes",
        "title": "Индексы в БД: ускорение SELECT и покрывающие индексы",
        "description": "Индексы ускоряют поиск, но не бесплатны. Учимся строить DDL-индекс, определять покрывающие индексы и выбирать лучший индекс под запрос.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "Index", "B-tree", "Производительность"],
        "learningOutcomes": [
            "Писать CREATE INDEX по колонке поиска",
            "Определять покрывающий индекс",
            "Выбирать индекс под предикат WHERE"
        ],
        "complexity": {
            "timeComplexity": "O(k) на задачу блока",
            "spaceComplexity": "O(1)–O(n)",
            "explanation": "Задачи проверяют логику выбора/построения индекса без реального SGBD."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какая структура данных типично лежит в основе индекса?",
                "options": [
                    {"id": "opt1", "text": "B-дерево", "isCorrect": True, "explanation": "Классический B-tree индекс."},
                    {"id": "opt2", "text": "Хэш-таблица всегда", "isCorrect": False, "explanation": "Хэш есть, но B-tree преобладает для диапазонов."},
                    {"id": "opt3", "text": "Один большой список", "isCorrect": False, "explanation": "Это обычное сканирование."}
                ],
                "hint": "Какое дерево поддерживает поиск и диапазоны за O(log n)?"
            },
            {
                "id": "q2",
                "question": "Когда индекс «покрывающий»?",
                "options": [
                    {"id": "opt1", "text": "Все нужные колонки есть в индексе (Index Only Scan)", "isCorrect": True, "explanation": "Тогда БД не ходит в таблицу."},
                    {"id": "opt2", "text": "Когда в индексе PK", "isCorrect": False, "explanation": "PK есть почти всегда, этого мало."},
                    {"id": "opt3", "text": "Когда индекс единственный", "isCorrect": False, "explanation": "Единственность индекса не связана с покрытием."}
                ],
                "hint": "Что надо, чтобы SELECT брал данные прямо из индекса?"
            }
        ],
        "attachedTasks": [
            {"taskId": "40-p1", "title": "DDL индекса", "difficulty": "easy", "slug": "create-index-sql"},
            {"taskId": "40-p2", "title": "Покрывающий индекс", "difficulty": "medium", "slug": "covering-index"},
            {"taskId": "40-p3", "title": "Лучший индекс под запрос", "difficulty": "hard", "slug": "best-index"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "CREATE INDEX idx_t_c ON t(c) ускоряет WHERE c=...",
                "SELECT из одних колонок индекса даёт Index Only Scan.",
                "Левые префиксы составного индекса ищутся максимально быстро.",
                "Индексы замедляют INSERT/UPDATE — их не должно быть слишком много."
            ]
        }
    },
    "problems": [
{
            "id": "40-p1", "title": "DDL индекса", "difficulty": "easy",
            "lecture_id": "40", "order": 1, "entry_function": "create_index_sql",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def create_index_sql(table: str, column: str) -> str:\n    \"\"\"Вернуть CREATE INDEX, ускоряющий поиск по column в table.\"\"\"\n    ...",
            "description": "Напишите функцию `create_index_sql(table, column)`, которая возвращает строку-команду `CREATE INDEX`, ускоряющую поиск по равенству `WHERE column = ...` в таблице `table`.\n\n**Формат:** `CREATE INDEX idx_<таблица>_<колонка> ON <таблица>(<колонка>);`\n\n**Функция решения:**\n\n```python\ndef create_index_sql(table: str, column: str) -> str:\n    ...\n```",
            "examples": [
                {"input": "create_index_sql('users', 'email')", "output": "CREATE INDEX idx_users_email ON users(email);", "explanation": "Индекс по уникальному поиску."},
                {"input": "create_index_sql('orders', 'created_at')", "output": "CREATE INDEX idx_orders_created_at ON orders(created_at);", "explanation": "Индекс для сортировки/диапазона."}
            ],
            "constraints": ["table и column — непустые строки"],
            "hints": [
                "Верните строку в строго заданном формате.",
                "Имя индекса: idx_<table>_<column>."
            ],
            "args": [
                ["users", "email"],
                ["orders", "created_at"],
                ["products", "sku"],
                ["users", "name"],
                ["logs", "ts"],
                ["orders", "total"]
            ],
            "hidden": [False, False, False, True, True, True]
        },
{
            "id": "40-p2", "title": "Покрывающий индекс", "difficulty": "medium",
            "lecture_id": "40", "order": 2, "entry_function": "is_covering_index",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def is_covering_index(select_cols: list[str], index_cols: list[str]) -> bool:\n    \"\"\"True, если индекс содержит все колонки из SELECT (покрывающий).\"\"\"\n    ...",
            "description": "Реализуйте `is_covering_index(select_cols, index_cols)`. Индекс называется **покрывающим**, если в нём содержатся все колонки, которые запрос выбирает в `SELECT` — тогда возможен `Index Only Scan` без обращения к таблице.\n\nВерните `True`, если **каждая** требуемая колонка из `select_cols` присутствует в составе индекса `index_cols`.\n\n**Функция решения:**\n\n```python\ndef is_covering_index(select_cols: list[str], index_cols: list[str]) -> bool:\n    ...\n```",
            "examples": [
                {"input": "is_covering_index(['email','id'], ['email','id'])", "output": "True", "explanation": "Обе колонки есть в индексе."},
                {"input": "is_covering_index(['email','name'], ['email','id'])", "output": "False", "explanation": "name нет в индексе."}
            ],
            "constraints": ["Дубликаты колонок не встречаются"],
            "hints": [
                "Проверьте включение: set(select_cols) <= set(index_cols).",
                "Порядок колонок в индексе не важен для покрытия."
            ],
            "args": [
                [["email", "id"], ["email", "id"]],
                [["email", "name"], ["email", "id"]],
                [["id"], ["id"]],
                [["email", "name", "age"], ["email", "name", "age"]],
                [["name"], ["email", "name"]],
                [["age"], ["name"]]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "40-p3", "title": "Лучший индекс под запрос", "difficulty": "hard",
            "lecture_id": "40", "order": 3, "entry_function": "best_index",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def best_index(where_cols: list[str], indexes: list[list[str]]) -> list[str]:\n    \"\"\"Вернуть индекс с максимальным совпадением левого префикса с WHERE-колонками.\"\"\"\n    ...",
            "description": "Из списка кандидатов `indexes` (каждый — список колонок) выберите тот составной индекс, который **наилучшим образом обслуживает предикаты `WHERE`** `where_cols`.\n\nПравило: индекс «полезен», если его колонки совпадают с `where_cols` **слева направо** — это называется совпадением левого префикса. Считаем **score = число подряд идущих колонок** индекса, совпавших с началом `where_cols`. Чем больше score — тем лучше. При равенстве возвращаем первый встреченный индекс.\n\nЕсли `indexes` пуст — верните пустой список.\n\n**Функция решения:**\n\n```python\ndef best_index(where_cols: list[str], indexes: list[list[str]]) -> list[str]:\n    ...\n```",
            "examples": [
                {"input": "best_index(['email'], [['name'], ['email']])", "output": "['email']", "explanation": "Индекс [email] даёт score 1, [name] — 0."},
                {"input": "best_index(['city','created_at'], [['city'], ['city','created_at']])", "output": "['city','created_at']", "explanation": "Составной индекс покрывает оба предиката."}
            ],
            "constraints": ["0 ≤ len(indexes) ≤ 10^3", "Колонки — строки"],
            "hints": [
                "Считайте ведущий префикс: пока index[i] == where_cols[i].",
                "Пустой indexes даёт пустой результат."
            ],
            "args": [
                [["email"], [["name"], ["email"]]],
                [["city", "created_at"], [["city"], ["city", "created_at"]]],
                [["user_id"], [["user_id", "created_at"], ["created_at"]]],
                [["status"], []],
                [["a", "b", "c"], [["a", "b"], ["a", "b", "c"]]],
                [["a"], [["a", "b"], ["a", "c"]]]
            ],
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])