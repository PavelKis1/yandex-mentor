"""Данные блока 37: SQL JOIN."""
from genlib import run
from sqllib import sql_cases

LECTURE_SLUG = "37_sql_join"

DDL = (
    "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);\n"
    "INSERT INTO users VALUES (1,'Ann'),(2,'Bob'),(3,'Cid'),(4,'Dev');\n"
    "CREATE TABLE orders(id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER);\n"
    "INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,3,200);\n"
)
DDL2 = (
    "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);\n"
    "INSERT INTO users VALUES (1,'Max'),(2,'Ada'),(3,'Leo'),(4,'Oli');\n"
    "CREATE TABLE orders(id INTEGER PRIMARY KEY, user_id INTEGER, amount INTEGER);\n"
    "INSERT INTO orders VALUES (1,3,90),(2,1,40);\n"
)

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "37",
        "slug": "sql-join",
        "title": "SQL JOIN: объединение таблиц",
        "description": "Объединение таблиц JOIN по ключу, типы JOIN и работа с NULL.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "Join", "LeftJoin", "ForeignKey"],
        "learningOutcomes": [
            "Писать INNER JOIN по внешнему ключу",
            "Осознавать разницу INNER vs LEFT JOIN и NULL-строки",
            "Применять JOIN с агрегатами (COUNT)"
        ],
        "complexity": {
            "timeComplexity": "O(a+b) hash join, O(n log n) merge join",
            "spaceComplexity": "O(a+b) при hash join",
            "explanation": "Оптимизатор выбирает Hash/Merge/Nested-loop в зависимости от данных."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой JOIN вернёт строки левой таблицы даже без совпадений?",
                "options": [
                    {"id": "opt1", "text": "LEFT JOIN", "isCorrect": True, "explanation": "LEFT JOIN сохраняет все строки левой таблицы, справа будет NULL."},
                    {"id": "opt2", "text": "INNER JOIN", "isCorrect": False, "explanation": "INNER JOIN оставляет только совпадения."},
                    {"id": "opt3", "text": "CROSS JOIN", "isCorrect": False, "explanation": "CROSS JOIN — декартово произведение."}
                ],
                "hint": "Какой JOIN не теряет строки левой таблицы?"
            },
            {
                "id": "q2",
                "question": "В LEFT JOIN нет совпадения в правой таблице. Что будет в колонках правой?",
                "options": [
                    {"id": "opt1", "text": "NULL", "isCorrect": True, "explanation": "Отсутствующие значения правой таблицы заполняются NULL."},
                    {"id": "opt2", "text": "0", "isCorrect": False, "explanation": "Это не 0, а NULL."},
                    {"id": "opt3", "text": "Пустая строка", "isCorrect": False, "explanation": "Это NULL."}
                ],
                "hint": "Чем заполняются отсутствующие значения?"
            }
        ],
        "attachedTasks": [
            {"taskId": "37-p1", "title": "Внутреннее соединение", "difficulty": "easy", "slug": "join-inner"},
            {"taskId": "37-p2", "title": "Левое соединение", "difficulty": "medium", "slug": "join-left"},
            {"taskId": "37-p3", "title": "JOIN с агрегацией", "difficulty": "hard", "slug": "join-aggregate"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "INNER JOIN — только совпадения по ключу.",
                "LEFT JOIN — все строки левой + NULL справа.",
                "ON задаёт условие сопоставления: a.id = b.user_id.",
                "Псевдонимы таблиц: FROM users u JOIN orders o.",
                "WITH LEFT JOIN подсчёт ведите через COUNT(o.id), не COUNT(*)."
            ]
        }
    },
    "problems": [
        {
            "sql": True, "id": "37-p1", "title": "Внутреннее соединение", "difficulty": "easy",
            "lecture_id": "37", "order": 1, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Даны таблицы `users(id, name)` и `orders(id, user_id, amount)`. Напишите запрос, который выводит имя пользователя и сумму заказа для **всех заказов**, используя `INNER JOIN`. Отсортируйте по `orders.id` (порядку добавления заказов).\n\n```sql\nSELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id ...;\n```",
            "examples": [
                {"input": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id ORDER BY o.id;",
                 "output": "Ann|100, Ann|50, Cid|200", "explanation": "У Dev нет заказов — в INNER JOIN его нет."}
            ],
            "constraints": ["INNER JOIN by u.id = o.user_id", "ORDER BY o.id"],
            "hints": ["FROM users u JOIN orders o ON u.id = o.user_id", "ORDER BY o.id"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id ORDER BY o.id;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id ORDER BY o.id;",
                 "hidden": True},
            ])
        },
{
            "sql": True, "id": "37-p2", "title": "Левое соединение", "difficulty": "medium",
            "lecture_id": "37", "order": 2, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Даны те же таблицы `users(id, name)` и `orders(id, user_id, amount)`. Напишите запрос с `LEFT JOIN`, который выводит **всех пользователей** (включая тех без заказов с `NULL` в сумме). Отсортируйте по имени пользователя.\n\n```sql\nSELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ...;\n```",
            "examples": [
                {"input": "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ORDER BY u.name;",
                 "output": "Ann|100, Ann|50, Bob|, Cid|200, Dev|", "explanation": "Bob и Dev без заказов — NULL."}
            ],
            "constraints": ["LEFT JOIN", "ORDER BY u.name"],
            "hints": ["LEFT JOIN orders o ON u.id = o.user_id", "У Bob и Dev сумма NULL"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ORDER BY u.name;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT u.name, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id ORDER BY u.name;",
                 "hidden": True},
            ])
        },
        {
            "sql": True, "id": "37-p3", "title": "JOIN с агрегацией", "difficulty": "hard",
            "lecture_id": "37", "order": 3, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Даны `users(id, name)` и `orders(id, user_id, amount)`. Напишите запрос, который для **каждого пользователя** считает количество его заказов `cnt` (у пользователей без заказов должно быть 0). Используйте `LEFT JOIN` + `GROUP BY`. Отсортируйте по убыванию `cnt`, при равенстве — по имени.\n\n```sql\nSELECT u.name, COUNT(o.id) AS cnt FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name ...;\n```",
            "examples": [
                {"input": "SELECT u.name, COUNT(o.id) AS cnt FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name ORDER BY cnt DESC, u.name;",
                 "output": "Ann|2, Cid|1, Bob|0, Dev|0", "explanation": "Считаем o.id, чтобы у беззаказных было 0."}
            ],
            "constraints": ["LEFT JOIN", "GROUP BY u.name", "COUNT(o.id)", "ORDER BY cnt DESC, name"],
            "hints": ["COUNT(o.id), а не COUNT(*)", "GROUP BY u.name", "ORDER BY cnt DESC, u.name"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT u.name, COUNT(o.id) AS cnt FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name ORDER BY cnt DESC, u.name;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT u.name, COUNT(o.id) AS cnt FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.name ORDER BY cnt DESC, u.name;",
                 "hidden": True},
            ])
        }
    ]
}

if __name__ == "__main__":
    run([meta])