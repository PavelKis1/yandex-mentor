"""Данные блока 36: SQL SELECT."""
from genlib import run
from sqllib import sql_cases

LECTURE_SLUG = "36_sql_select"

DDL_USERS = (
    "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, age INTEGER);\n"
    "INSERT INTO users VALUES (1,'Ann',25),(2,'Bob',17),(3,'Cid',30),"
    "(4,'Dev',19),(5,'Eva',22),(6,'Fay',17);\n"
)
DDL_USERS2 = (
    "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, age INTEGER);\n"
    "INSERT INTO users VALUES (1,'Max',41),(2,'Ada',15),(3,'Leo',28);\n"
)
DDL_USERS3 = (
    "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, age INTEGER);\n"
    "INSERT INTO users VALUES (1,'Zed',20),(2,'Amy',35),(3,'Oz',10),(4,'Uli',16);\n"
)

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "36",
        "slug": "sql-select",
        "title": "SQL SELECT: проекция, фильтр, сортировка, LIMIT",
        "description": "Получение данных: SELECT, FROM, WHERE, ORDER BY, LIMIT, псевдонимы и CASE.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "Select", "Where", "OrderBy"],
        "learningOutcomes": [
            "Писать SELECT с проекцией колонок и псевдонимами",
            "Фильтровать через WHERE (>, BETWEEN, LIKE)",
            "Сортировать и ограничивать выборку ORDER BY + LIMIT"
        ],
        "complexity": {
            "timeComplexity": "O(n) выборка, O(n log n) с сортировкой",
            "spaceComplexity": "O(n) на буфер результатов",
            "explanation": "Сложность зависит от индексов и необходимости сортировки."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой оператор фильтрует строки до GROUP BY?",
                "options": [
                    {"id": "opt1", "text": "WHERE", "isCorrect": True, "explanation": "WHERE фильтрует строки, HAVING — группы."},
                    {"id": "opt2", "text": "HAVING", "isCorrect": False, "explanation": "HAVING применяется к группам."},
                    {"id": "opt3", "text": "LIMIT", "isCorrect": False, "explanation": "LIMIT ограничивает число строк."}
                ],
                "hint": "Что применяется раньше — фильтр строк или группировка?"
            },
            {
                "id": "q2",
                "question": "Что вернёт SELECT name FROM users ORDER BY age DESC LIMIT 3?",
                "options": [
                    {"id": "opt1", "text": "Три самых старших пользователя", "isCorrect": True, "explanation": "Сортировка по убыванию возраста и ограничение 3 строками."},
                    {"id": "opt2", "text": "Три самых молодых", "isCorrect": False, "explanation": "DESC — по убыванию, значит старшие."},
                    {"id": "opt3", "text": "Всех пользователей", "isCorrect": False, "explanation": "LIMIT 3 обрезает до трёх."}
                ],
                "hint": "Что делает DESC?"
            }
        ],
        "attachedTasks": [
            {"taskId": "36-p1", "title": "Выборка с условием", "difficulty": "easy", "slug": "select-adults"},
            {"taskId": "36-p2", "title": "Проекция и LIMIT", "difficulty": "medium", "slug": "select-top"},
            {"taskId": "36-p3", "title": "CASE и шаблоны", "difficulty": "hard", "slug": "select-case"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "SELECT колонки FROM таблица WHERE условие.",
                "ORDER BY колонка [ASC|DESC] — сортировка.",
                "LIMIT n ограничивает число строк.",
                "CASE WHEN ... THEN ... END — условный столбец; LIKE — шаблон строки.",
                "Псевдоним AS переименовывает колонку."
            ]
        }
    },
    "problems": [
        {
            "sql": True, "id": "36-p1", "title": "Выборка с условием", "difficulty": "easy",
            "lecture_id": "36", "order": 1, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `users(id, name, age)`. Напишите запрос, который выбирает имя и возраст пользователей **старше 18 лет**, отсортировав их **по убыванию возраста**, а при равном возрасте — по имени (по возрастанию).\n\n```sql\nSELECT name, age FROM users ...;\n```",
            "examples": [
                {"input": "SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC, name;",
                 "output": "Cid|30, Ann|25, Eva|22, Dev|19", "explanation": "Только взрослые, старший первым."}
            ],
            "constraints": ["age > 18", "ORDER BY age DESC, name ASC"],
            "hints": ["WHERE age > 18", "ORDER BY age DESC, name"],
            "cases": sql_cases([
                {"ddl": DDL_USERS,
                 "query": "SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC, name;",
                 "hidden": False},
                {"ddl": DDL_USERS2,
                 "query": "SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC, name;",
                 "hidden": True},
            ])
        },
        {
            "sql": True, "id": "36-p2", "title": "Проекция и LIMIT", "difficulty": "medium",
            "lecture_id": "36", "order": 2, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `users(id, name, age)`. Напишите запрос, который выводит **топ-3 самых старших** пользователя с псевдонимом колонки `years` для возраста: `SELECT name, age AS years FROM users ...`. При равном возрасте сортируйте по имени.\n\n```sql\nSELECT name, age AS years FROM users ... LIMIT 3;\n```",
            "examples": [
                {"input": "SELECT name, age AS years FROM users ORDER BY age DESC, name LIMIT 3;",
                 "output": "Cid|30, Ann|25, Eva|22", "explanation": "Три старших в первой таблице."}
            ],
            "constraints": ["LIMIT 3", "псевдоним years = age"],
            "hints": ["ORDER BY age DESC, name", "LIMIT 3;  AS years"],
            "cases": sql_cases([
                {"ddl": DDL_USERS,
                 "query": "SELECT name, age AS years FROM users ORDER BY age DESC, name LIMIT 3;",
                 "hidden": False},
                {"ddl": DDL_USERS3,
                 "query": "SELECT name, age AS years FROM users ORDER BY age DESC, name LIMIT 3;",
                 "hidden": True},
            ])
        },
        {
            "sql": True, "id": "36-p3", "title": "CASE и шаблоны", "difficulty": "hard",
            "lecture_id": "36", "order": 3, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `users(id, name, age)`. Напишите запрос, который для каждого пользователя, чьё имя **начинается на 'A'** (`name LIKE 'A%'`) и возраст от **18 до 30 включительно**, выводит имя и статус: `'adult'`, если возраст ≥ 18, иначе `'minor'`. Отсортируйте по имени.\n\n```sql\nSELECT name, CASE WHEN age >= 18 THEN 'adult' ELSE 'minor' END AS status FROM users ...;\n```",
            "examples": [
                {"input": "SELECT name, CASE WHEN age>=18 THEN 'adult' ELSE 'minor' END AS status FROM users WHERE age BETWEEN 18 AND 30 AND name LIKE 'A%' ORDER BY name;",
                 "output": "Ann|adult", "explanation": "Только Ann подходит под фильтры."}
            ],
            "constraints": ["name LIKE 'A%'", "age BETWEEN 18 AND 30"],
            "hints": ["CASE WHEN age>=18 THEN 'adult' ELSE 'minor' END", "LIKE 'A%'", "BETWEEN 18 AND 30"],
            "cases": sql_cases([
                {"ddl": DDL_USERS,
                 "query": "SELECT name, CASE WHEN age>=18 THEN 'adult' ELSE 'minor' END AS status FROM users WHERE age BETWEEN 18 AND 30 AND name LIKE 'A%' ORDER BY name;",
                 "hidden": False},
                {"ddl": DDL_USERS3,
                 "query": "SELECT name, CASE WHEN age>=18 THEN 'adult' ELSE 'minor' END AS status FROM users WHERE age BETWEEN 18 AND 30 AND name LIKE 'A%' ORDER BY name;",
                 "hidden": True},
            ])
        }
    ]
}

if __name__ == "__main__":
    run([meta])