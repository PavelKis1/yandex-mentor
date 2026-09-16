"""Данные блока 38: SQL GROUP BY."""
from genlib import run
from sqllib import sql_cases

LECTURE_SLUG = "38_sql_groupby"

DDL = (
    "CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT, amount INTEGER);\n"
    "INSERT INTO orders VALUES (1,'new',100),(2,'done',50),(3,'new',200),"
    "(4,'done',30),(5,'cancel',10);\n"
)
DDL2 = (
    "CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT, amount INTEGER);\n"
    "INSERT INTO orders VALUES (1,'new',30),(2,'done',200),(3,'new',40),"
    "(4,'cancel',5),(5,'done',60),(6,'new',10);\n"
)

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "38",
        "slug": "sql-groupby",
        "title": "SQL GROUP BY и агрегатные функции",
        "description": "Агрегация данных: COUNT, SUM, MIN, MAX, фильтрация групп через HAVING.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "GroupBy", "Aggregates", "Having"],
        "learningOutcomes": [
            "Группировать строки через GROUP BY",
            "Применять COUNT, SUM, MIN, MAX",
            "Фильтровать группы через HAVING"
        ],
        "complexity": {
            "timeComplexity": "O(n log n) сортировка либо O(n) при хэшировании",
            "spaceComplexity": "O(k) на число групп",
            "explanation": "Агрегация сверяется по ключам групп."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Чем HAVING отличается от WHERE?",
                "options": [
                    {"id": "opt1", "text": "HAVING фильтрует группы после GROUP BY", "isCorrect": True, "explanation": "WHERE — строки до группировки, HAVING — группы после."},
                    {"id": "opt2", "text": "Это синонимы", "isCorrect": False, "explanation": "Нет, применяются на разных этапах."},
                    {"id": "opt3", "text": "WHERE для подзапросов", "isCorrect": False, "explanation": "Неверно."}
                ],
                "hint": "Где можно использовать агрегатные функции в условии?"
            },
            {
                "id": "q2",
                "question": "Что вернёт COUNT(*) для группы, в которой 3 строки?",
                "options": [
                    {"id": "opt1", "text": "3", "isCorrect": True, "explanation": "COUNT(*) считает все строки группы."},
                    {"id": "opt2", "text": "0", "isCorrect": False, "explanation": "Веду как число строк."},
                    {"id": "opt3", "text": "NULL", "isCorrect": False, "explanation": "Без NULL здесь."}
                ],
                "hint": "Сколько строк в группе?"
            }
        ],
        "attachedTasks": [
            {"taskId": "38-p1", "title": "Счётчик по группам", "difficulty": "easy", "slug": "groupby-count"},
            {"taskId": "38-p2", "title": "Сумма и HAVING", "difficulty": "medium", "slug": "groupby-sum"},
            {"taskId": "38-p3", "title": "Фильтр групп", "difficulty": "hard", "slug": "groupby-having"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "GROUP BY колонка сворачивает строки в группы.",
                "COUNT(*), SUM(x), AVG(x), MIN(x), MAX(x) — агрегаты.",
                "HAVING — фильтр по агрегату, WHERE — по строке.",
                "В SELECT при GROUP BY можно брать только сгруппированные колонки и агрегаты."
            ]
        }
    },
    "problems": [
        {
            "sql": True, "id": "38-p1", "title": "Счётчик по группам", "difficulty": "easy",
            "lecture_id": "38", "order": 1, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `orders(id, status, amount)`. Напишите запрос, который для каждого `status` считает число заказов `cnt`. Отсортируйте по убыванию `cnt`, при равенстве — по статусу.\n\n```sql\nSELECT status, COUNT(*) AS cnt FROM orders GROUP BY status ...;\n```",
            "examples": [
                {"input": "SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status ORDER BY cnt DESC, status;",
                 "output": "done|2, new|2, cancel|1", "explanation": "done и new по 2, cancel — 1; при равенстве по алфавиту."}
            ],
            "constraints": ["GROUP BY status", "COUNT(*)", "ORDER BY cnt DESC, status"],
            "hints": ["GROUP BY status", "COUNT(*) AS cnt", "ORDER BY cnt DESC, status"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status ORDER BY cnt DESC, status;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT status, COUNT(*) AS cnt FROM orders GROUP BY status ORDER BY cnt DESC, status;",
                 "hidden": True},
            ])
        },{
            "sql": True, "id": "38-p2", "title": "Сумма и HAVING", "difficulty": "medium",
            "lecture_id": "38", "order": 2, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `orders(id, status, amount)`. Напишите запрос, который для каждого `status`, где **не менее двух заказов** (`COUNT(*) >= 2`), выводит суммарный `amount` как `total`. Отсортируйте по убыванию `total`.\n\n```sql\nSELECT status, SUM(amount) AS total FROM orders GROUP BY status ...;\n```",
            "examples": [
                {"input": "SELECT status, SUM(amount) AS total FROM orders GROUP BY status HAVING COUNT(*) >= 2 ORDER BY total DESC;",
                 "output": "new|300, done|80", "explanation": "cancel — один заказ, выбывает через HAVING."}
            ],
            "constraints": ["GROUP BY status", "SUM(amount)", "HAVING COUNT(*) >= 2", "ORDER BY total DESC"],
            "hints": ["HAVING COUNT(*) >= 2", "SUM(amount) AS total", "ORDER BY total DESC"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT status, SUM(amount) AS total FROM orders GROUP BY status HAVING COUNT(*) >= 2 ORDER BY total DESC;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT status, SUM(amount) AS total FROM orders GROUP BY status HAVING COUNT(*) >= 2 ORDER BY total DESC;",
                 "hidden": True},
            ])
        },
        {
            "sql": True, "id": "38-p3", "title": "Фильтр групп", "difficulty": "hard",
            "lecture_id": "38", "order": 3, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `orders(id, status, amount)`. Напишите запрос, который возвращает статусы, у которых **суммарный `amount` больше 50** (`SUM(amount) > 50`). Отсортируйте по статусу.\n\n```sql\nSELECT status FROM orders GROUP BY status HAVING SUM(amount) > 50 ORDER BY status;\n```",
            "examples": [
                {"input": "SELECT status FROM orders GROUP BY status HAVING SUM(amount) > 50 ORDER BY status;",
                 "output": "done, new", "explanation": "new=300 и done=80 больше 50, cancel=10 выбывает."}
            ],
            "constraints": ["GROUP BY status", "HAVING SUM(amount) > 50", "ORDER BY status"],
            "hints": ["HAVING SUM(amount) > 50", "SELECT status", "ORDER BY status"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT status FROM orders GROUP BY status HAVING SUM(amount) > 50 ORDER BY status;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT status FROM orders GROUP BY status HAVING SUM(amount) > 50 ORDER BY status;",
                 "hidden": True},
            ])
        }
    ]
}

if __name__ == "__main__":
    run([meta])