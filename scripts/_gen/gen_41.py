"""Данные блока 41: EXPLAIN планов запросов (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "41_explain"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "41",
        "slug": "explain",
        "title": "Читаем EXPLAIN: типы сканирования, оценки и стоимость",
        "description": "Планировщик строит план запроса. Учимся распознавать эффективные и неэффективные типы сканирования, читать оценку строк и считать стоимость соединений.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "EXPLAIN", "Query Planner", "Производительность"],
        "learningOutcomes": [
            "Отличать эффективные типы сканирования от Seq Scan",
            "Читать оценку строк из плана",
            "Оценивать стоимость Hash Join"
        ],
        "complexity": {
            "timeComplexity": "O(n) на задачи блока",
            "spaceComplexity": "O(1)",
            "explanation": "Задачи проверяют умение интерпретировать текстовый план EXPLAIN."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой тип сканирования считается самым медленным при полном просмотре таблицы?",
                "options": [
                    {"id": "opt1", "text": "ALL / Seq Scan", "isCorrect": True, "explanation": "Полное сканирование всей таблицы."},
                    {"id": "opt2", "text": "index", "isCorrect": False, "explanation": "Идёт через индекс — быстрее."},
                    {"id": "opt3", "text": "const", "isCorrect": False, "explanation": "Доступ по ключу за одну строку."}
                ],
                "hint": "Как называется полный проход по всем строкам?"
            },
            {
                "id": "q2",
                "question": "Что показывает `rows` в узле EXPLAIN?",
                "options": [
                    {"id": "opt1", "text": "Оценку планировщика числа строк узла", "isCorrect": True, "explanation": "Это оценка, а не факт."},
                    {"id": "opt2", "text": "Точное число строк из таблицы", "isCorrect": False, "explanation": "Без ANALYZE точность не гарантируется."},
                    {"id": "opt3", "text": "Число колонок", "isCorrect": False, "explanation": "Колонки — это width."}
                ],
                "hint": "План строится до выполнения — числа оценочные."
            }
        ],
        "attachedTasks": [
            {"taskId": "41-p1", "title": "Эффективность плана", "difficulty": "easy", "slug": "plan-efficiency"},
            {"taskId": "41-p2", "title": "Оценка строк", "difficulty": "medium", "slug": "parse-rows"},
            {"taskId": "41-p3", "title": "Стоимость соединения", "difficulty": "hard", "slug": "join-cost"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "ALL / Seq Scan — полный перебор, плохо на больших таблицах.",
                "const/eq_ref/ref/range/index — эффективные типы.",
                "rows=NNN — оценка кардинальности узла.",
                "Hash Join стоит примерно left × right × selectivity строк."
            ]
        }
    },
    "problems": [
{
            "id": "41-p1", "title": "Эффективность плана", "difficulty": "easy",
            "lecture_id": "41", "order": 1, "entry_function": "plan_is_efficient",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def plan_is_efficient(scan_type: str) -> bool:\n    \"\"\"True, если тип сканирования эффективен (не полный перебор таблицы).\"\"\"\n    ...",
            "description": "Планировщик указывает тип сканирования. Полный просмотр таблицы (`ALL`, `Seq Scan`, `sequential scan`) — самый медленный вариант. Прочие типы (`index`, `ref`, `eq_ref`, `range`, `const`, `Index Only Scan`) считаем эффективными.\n\nРеализуйте `plan_is_efficient(scan_type)`, возвращающую `False`, если тип означает **полное сканирование**, и `True` иначе.\n\nСчитаются «плохими» (независимо от регистра): `all`, `seq`, `seq_scan`, `seq scan`, `full scan`, `sequential scan`.\n\n**Функция решения:**\n\n```python\ndef plan_is_efficient(scan_type: str) -> bool:\n    ...\n```",
            "examples": [
                {"input": "plan_is_efficient('ALL')", "output": "False", "explanation": "Полный перебор таблицы — плохо."},
                {"input": "plan_is_efficient('ref')", "output": "True", "explanation": "Поиск по не уникальному индексу."}
            ],
            "constraints": ["scan_type — непустая строка"],
            "hints": [
                "Приведите к нижнему регистру и отбросьте пробелы.",
                "Сравните со списком «полных сканирований»."
            ],
            "args": [["ALL"], ["index"], ["ref"], ["Seq Scan"]],
            "hidden": [False, False, False, True]
        },
        {
            "id": "41-p2", "title": "Оценка строк", "difficulty": "medium",
            "lecture_id": "41", "order": 2, "entry_function": "parse_explain_rows",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def parse_explain_rows(text: str):\n    \"\"\"Вынуть число rows=N из текста EXPLAIN (int или None).\"\"\"\n    ...",
            "description": "В выводе `EXPLAIN` планировщик оценивает число строк узла как `rows=N`. Напишите `parse_explain_rows(text)`, которая извлекает целое число `N` из фрагмента `rows=NNN`.\n\nЕсли в тексте нет совпадения `rows=NNN` — верните `None`.\n\n**Функция решения:**\n\n```python\ndef parse_explain_rows(text: str):\n    ...\n```",
            "examples": [
                {"input": "parse_explain_rows('seq scan on users (cost=0.00..35.50 rows=1000 width=8)')", "output": "1000", "explanation": "Планировщик ожидает 1000 строк."},
                {"input": "parse_explain_rows('no rows here')", "output": "None", "explanation": "Нет паттерна rows=NNN."}
            ],
            "constraints": ["text — строка", "Искомая N — целое"],
            "hints": [
                "Regex r'rows=(\\d+)' находит число.",
                "Используйте .search, а не .match."
            ],
            "args": [
                ["seq scan on users (cost=0.00..35.50 rows=1000 width=8)"],
                ["index scan on orders using idx (cost=0.28..8.30 rows=25 width=6)"],
                ["hash (cost=40.21..40.21 rows=300 width=4)"],
                ["explain analyze select * from t where id=5 rows=1"]
            ],
            "hidden": [False, False, False, True]
        },
        {
            "id": "41-p3", "title": "Стоимость соединения", "difficulty": "hard",
            "lecture_id": "41", "order": 3, "entry_function": "estimate_join_rows",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def estimate_join_rows(left_rows: int, right_rows: int, selectivity: float) -> int:\n    \"\"\"Оценочное число строк Hash Join: округлить left * right * selectivity.\"\"\"\n    ...",
            "description": "Хэш-соединение возвращает примерно `left × right × selectivity` строк, где `left_rows` и `right_rows` — мощности таблиц, а `selectivity` (0–1) — доля совпадающих ключей.\n\nРеализуйте `estimate_join_rows(left_rows, right_rows, selectivity)`, возвращающую результат, **округлённый до ближайшего целого**.\n\n**Функция решения:**\n\n```python\ndef estimate_join_rows(left_rows: int, right_rows: int, selectivity: float) -> int:\n    ...\n```",
            "examples": [
                {"input": "estimate_join_rows(1000, 100, 0.1)", "output": "10000", "explanation": "1000×100×0.1 = 10000."},
                {"input": "estimate_join_rows(10, 10, 1.0)", "output": "100", "explanation": "Полное соединение всех строк."}
            ],
            "constraints": ["left_rows, right_rows ≥ 0", "0 ≤ selectivity ≤ 1"],
            "hints": [
                "Перемножьте и примените round().",
                "round(3.0) == 3 — целое."
            ],
            "args": [[1000, 100, 0.1], [10, 10, 1.0], [500, 200, 0.5], [100, 100, 0.01]],
            "hidden": [False, False, False, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])