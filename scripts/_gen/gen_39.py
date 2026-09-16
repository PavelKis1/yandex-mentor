"""Данные блока 39: SQL Window Functions."""
from genlib import run
from sqllib import sql_cases

LECTURE_SLUG = "39_sql_window"

DDL = (
    "CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER);\n"
    "INSERT INTO employees VALUES (1,'Ann','Eng',100),(2,'Bob','Eng',120),"
    "(3,'Cid','Ops',90),(4,'Dev','Ops',150),(5,'Eva','Eng',110);\n"
)
DDL2 = (
    "CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER);\n"
    "INSERT INTO employees VALUES (1,'Mae','Eng',80),(2,'Noa','Ops',70),"
    "(3,'Rex','Eng',130),(4,'Ida','Ops',70),(5,'Zoe','Ops',90);\n"
)

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "39",
        "slug": "sql-window",
        "title": "SQL Window Functions",
        "description": "Оконные функции: OVER, PARTITION BY, ROW_NUMBER, RANK, LAG, движущиеся агрегаты.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "Window", "Over", "Partition", "RowNumber"],
        "learningOutcomes": [
            "Ранжировать строки через ROW_NUMBER() OVER (ORDER BY ...)",
            "Вычислять агрегаты по окну через PARTITION BY",
            "Получать соседние строки через LAG"
        ],
        "complexity": {
            "timeComplexity": "O(n log n) из-за сортировки в окне",
            "spaceComplexity": "O(n) на окно",
            "explanation": "Оконные функции не сворачивают строки, а лишь добавляют вычисленные колонки."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что делает ROW_NUMBER() OVER (ORDER BY salary DESC)?",
                "options": [
                    {"id": "opt1", "text": "Нумерует строки от 1 по убыванию зарплаты", "isCorrect": True, "explanation": "ROW_NUMBER присваивает уникальный номер в порядке окна."},
                    {"id": "opt2", "text": "Сворачивает строки в группы", "isCorrect": False, "explanation": "Это делает GROUP BY."},
                    {"id": "opt3", "text": "Считает сумму зарплат", "isCorrect": False, "explanation": "Это агрегат SUM."}
                ],
                "hint": "Что возвращает ROW_NUMBER для каждой строки?"
            },
            {
                "id": "q2",
                "question": "Что вернёт LAG(salary) для первой строки окна?",
                "options": [
                    {"id": "opt1", "text": "NULL", "isCorrect": True, "explanation": "До первой строки окна нет предыдущей, поэтому NULL."},
                    {"id": "opt2", "text": "0", "isCorrect": False, "explanation": "Это NULL, а не 0."},
                    {"id": "opt3", "text": "Саму зарплату", "isCorrect": False, "explanation": "LAG берёт предыдущую строку."}
                ],
                "hint": "Что стоит до начала окна?"
            }
        ],
        "attachedTasks": [
            {"taskId": "39-p1", "title": "Нумерация строк", "difficulty": "easy", "slug": "window-rownumber"},
            {"taskId": "39-p2", "title": "Агрегат по окну", "difficulty": "medium", "slug": "window-avg"},
            {"taskId": "39-p3", "title": "Соседние строки", "difficulty": "hard", "slug": "window-lag"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "OVER (ORDER BY ...) задаёт окно для вычислений.",
                "ROW_NUMBER(), RANK(), DENSE_RANK() ранжируют строки.",
                "PARTITION BY делит данные на независимые окна.",
                "LAG(x)/LEAD(x) обращаются к соседним строкам.",
                "Оконные функции не сворачивают строки, в отличие от GROUP BY."
            ]
        }
    },
    "problems": [
        {
            "sql": True, "id": "39-p1", "title": "Нумерация строк", "difficulty": "easy",
            "lecture_id": "39", "order": 1, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `employees(id, name, department, salary)`. Напишите запрос, который нумерует сотрудников от 1 по **убыванию зарплаты** (`rn`), при одинаковой зарплате — по имени. Отсортируйте по `rn`.\n\n```sql\nSELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, name) AS rn FROM employees ORDER BY rn;\n```",
            "examples": [
                {"input": "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, name) AS rn FROM employees ORDER BY rn;",
                 "output": "Dev|150|1, Bob|120|2, Eva|110|3, Ann|100|4, Cid|90|5", "explanation": "Самый высокооплачиваемый получает 1."}
            ],
            "constraints": ["ROW_NUMBER() OVER (ORDER BY salary DESC, name)", "ORDER BY rn"],
            "hints": ["ROW_NUMBER() OVER (ORDER BY salary DESC, name)", "AS rn", "ORDER BY rn"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, name) AS rn FROM employees ORDER BY rn;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC, name) AS rn FROM employees ORDER BY rn;",
                 "hidden": True},
            ])
        },{
            "sql": True, "id": "39-p2", "title": "Агрегат по окну", "difficulty": "medium",
            "lecture_id": "39", "order": 2, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `employees(id, name, department, salary)`. Напишите запрос, который для каждого сотрудника показывает среднюю зарплату его **департамента** `dept_avg` (округлённую до 1 знака) через `AVG(...) OVER (PARTITION BY department)`. Отсортируйте по `id`.\n\n```sql\nSELECT name, department, ROUND(AVG(salary) OVER (PARTITION BY department), 1) AS dept_avg FROM employees ORDER BY id;\n```",
            "examples": [
                {"input": "SELECT name, department, ROUND(AVG(salary) OVER (PARTITION BY department),1) AS dept_avg FROM employees ORDER BY id;",
                 "output": "Ann|Eng|110.0, Bob|Eng|110.0, Cid|Ops|120.0, Dev|Ops|120.0, Eva|Eng|110.0",
                 "explanation": "Eng: (100+120+110)/3=110; Ops: (90+150)/2=120."}
            ],
            "constraints": ["AVG(salary) OVER (PARTITION BY department)", "ROUND(..., 1)", "ORDER BY id"],
            "hints": ["AVG(salary) OVER (PARTITION BY department)", "ROUND(...,1)", "ORDER BY id"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT name, department, ROUND(AVG(salary) OVER (PARTITION BY department),1) AS dept_avg FROM employees ORDER BY id;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT name, department, ROUND(AVG(salary) OVER (PARTITION BY department),1) AS dept_avg FROM employees ORDER BY id;",
                 "hidden": True},
            ])
        },
        {
            "sql": True, "id": "39-p3", "title": "Соседние строки", "difficulty": "hard",
            "lecture_id": "39", "order": 3, "lecture_slug": LECTURE_SLUG,
            "starter_code": "",
            "description": "Дана таблица `employees(id, name, department, salary)`. Напишите запрос, который для каждого сотрудника показывает зарплату **предыдущего сотрудника в его департаменте** по возрастанию зарплаты (`prev`) через `LAG`. У первого в департаменте `prev` — `NULL`. Отсортируйте по `department`, затем по `salary`.\n\n```sql\nSELECT name, salary, LAG(salary) OVER (PARTITION BY department ORDER BY salary, name) AS prev FROM employees ORDER BY department, salary;\n```",
            "examples": [
                {"input": "SELECT name, salary, LAG(salary) OVER (PARTITION BY department ORDER BY salary, name) AS prev FROM employees ORDER BY department, salary;",
                 "output": "Ann|100|, Eva|110|100, Bob|120|110, Cid|90|, Dev|150|90",
                 "explanation": "Ann и Cid — первые в своих отделах, prev = NULL."}
            ],
            "constraints": ["LAG(salary) OVER (PARTITION BY department ORDER BY salary, name)", "ORDER BY department, salary"],
            "hints": ["LAG(salary) OVER (PARTITION BY department ORDER BY salary, name)", "ORDER BY department, salary"],
            "cases": sql_cases([
                {"ddl": DDL,
                 "query": "SELECT name, salary, LAG(salary) OVER (PARTITION BY department ORDER BY salary, name) AS prev FROM employees ORDER BY department, salary;",
                 "hidden": False},
                {"ddl": DDL2,
                 "query": "SELECT name, salary, LAG(salary) OVER (PARTITION BY department ORDER BY salary, name) AS prev FROM employees ORDER BY department, salary;",
                 "hidden": True},
            ])
        }
    ]
}

if __name__ == "__main__":
    run([meta])