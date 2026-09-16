"""Данные блока 34: Dataclasses (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "34_dataclasses"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "34",
        "slug": "dataclasses",
        "title": "Dataclasses: равенство, сортировка, replace",
        "description": "dataclass автоматически генерирует eq/ordering/repr. Разбираем равенство экземпляров, сортировку заказов и объединение полей через replace.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Dataclasses", "OO"],
        "learningOutcomes": [
            "Описывать dataclass с типизированными полями",
            "Использовать сгенерированное eq и ordering",
            "Копировать/менять поля через dataclasses.replace"
        ],
        "complexity": {
            "timeComplexity": "O(n log n) для сортировки",
            "spaceComplexity": "O(n)",
            "explanation": "Равенство и конструкторы O(1) на экземпляр; сортировка заказов — O(n log n)."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что генерирует @dataclass(eq=True) по умолчанию?",
                "options": [
                    {"id": "opt1", "text": "Метод __eq__, сравнивающий все поля", "isCorrect": True, "explanation": "Экземпляры равны, если все поля совпадают."},
                    {"id": "opt2", "text": "Метод __lt__ для сортировки", "isCorrect": False, "explanation": "Для сортировки нужен order=True."},
                    {"id": "opt3", "text": "Ничего", "isCorrect": False, "explanation": "eq=True включён по умолчанию."}
                ],
                "hint": "Что сравнивает == для dataclass?"
            },
            {
                "id": "q2",
                "question": "Зачем dataclasses.replace?",
                "options": [
                    {"id": "opt1", "text": "Создать копию с изменением отдельных полей", "isCorrect": True, "explanation": "replace копирует объект, переопределяя указанные поля."},
                    {"id": "opt2", "text": "Удалить поля", "isCorrect": False, "explanation": "replace не удаляет поля."},
                    {"id": "opt3", "text": "Отсортировать", "isCorrect": False, "explanation": "Для сортировки есть sorted."}
                ],
                "hint": "Как не мутировать исходный объект, но поменять поле?"
            }
        ],
        "attachedTasks": [
            {"taskId": "34-p1", "title": "Сравнение пользователей", "difficulty": "easy", "slug": "compare-users"},
            {"taskId": "34-p2", "title": "Сортировка заказов", "difficulty": "medium", "slug": "sort-orders"},
            {"taskId": "34-p3", "title": "Объединение dataclass", "difficulty": "hard", "slug": "merge-users"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "@dataclass добавляет __init__, __repr__ и __eq__ по умолчанию.",
                "order=True добавляет методы сравнения для sorted().",
                "dataclasses.replace(obj, field=val) — не мутирует исходный объект.",
                "Поля с default или default_factory упрощают конструирование."
            ]
        }
    },
    "problems": [
        {
            "id": "34-p1", "title": "Сравнение пользователей", "difficulty": "easy",
            "lecture_id": "34", "order": 1, "entry_function": "compare_users",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "from dataclasses import dataclass\n\n@dataclass\nclass User:\n    ...\n\ndef compare_users(u1: list, u2: list) -> bool:\n    \"\"\"u1, u2 — [id, name, email]; построить двух User и вернуть u1 == u2.\"\"\"\n    ...",
            "description": "Опишите датакласс `User` с полями `id: int`, `name: str`, `email: str`. Функция `compare_users(u1, u2)` принимает двух пользователей как списки `[id, name, email]`, строит из них экземпляры `User` и возвращает `True`, если они **равны** (сгенерированный `__eq__` сравнивает все поля).\n\n**Функция решения:**\n\n```python\ndef compare_users(u1: list, u2: list) -> bool:\n    ...\n```",
            "examples": [
                {"input": "u1 = [1,'Ann','a@b'], u2 = [1,'Ann','a@b']", "output": "True", "explanation": "Все поля совпадают."},
                {"input": "u1 = [1,'Ann','a@b'], u2 = [1,'Ann','c@d']", "output": "False", "explanation": "Отличается email."}
            ],
            "constraints": ["id: int; name, email: str"],
            "hints": [
                "User(*u1) == User(*u2) — работает благодаря eq=True.",
                "Поля: id:int, name:str, email:str."
            ],
            "args": [
                [[1, "Ann", "a@b"], [1, "Ann", "a@b"]],
                [[1, "Ann", "a@b"], [1, "Ann", "c@d"]],
                [[2, "B", "b"], [2, "B", "b"]],
                [[1, "A", "x"], [2, "A", "x"]],
                [[7, "I", "i"], [7, "J", "i"]],
                [[0, "", ""], [0, "", ""]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "34-p2", "title": "Сортировка заказов", "difficulty": "medium",
            "lecture_id": "34", "order": 2, "entry_function": "sort_orders",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "@dataclass(order=True)\nclass Order:\n    ...\n\ndef sort_orders(orders: list) -> list:\n    \"\"\"Отсортировать [[id,total],...] по total убыв., затем по id возр.; вернуть списки [id,total].\"\"\"\n    ...",
            "description": "Опишите датакласс `Order(id: int, total: float)` с `order=True` и настройте порядок так, чтобы `sorted(orders)` шёл **по убыванию** `total`, затем **по возрастанию** `id` (используйте поле сортировки или `sort_index`). Функция `sort_orders(orders)` принимает заказы как `[[id, total], ...]` и возвращает отсортированные заказы списками `[id, total]`.\n\n**Функция решения:**\n\n```python\ndef sort_orders(orders: list) -> list:\n    ...\n```",
            "examples": [
                {"input": "orders = [[1,10.5],[2,3.0],[3,10.5]]", "output": "[[1,10.5],[3,10.5],[2,3.0]]", "explanation": "По total убыв.; при равных total — по id возр."}
            ],
            "constraints": ["id: int; total: float"],
            "hints": [
                "Проще всего: sorted(orders, key=lambda o: (-o[1], o[0])).",
                "Если хотите через dataclass — добавьте sort_index и order=True."
            ],
            "args": [
                [[[1, 10.5], [2, 3.0], [3, 10.5]]],
                [[[5, 1.0]]],
                [[[1, 2.0], [2, 2.0], [3, 2.0]]],
                [[[4, 9.9], [1, 0.1]]],
                [[[2, 5.0], [1, 5.0], [3, 5.0]]],
                [[[1, 100.0], [2, 50.0], [3, 75.0], [4, 75.0]]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "34-p3", "title": "Объединение dataclass", "difficulty": "hard",
            "lecture_id": "34", "order": 3, "entry_function": "merge_users",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def merge_users(a: list, b: list) -> list:\n    \"\"\"a, b — [id,name,email]; вернуть [id,name,email] нового User: поля a, но email=b.email если у a пустой email.\"\"\"\n    ...",
            "description": "Напишите `merge_users(a, b)`, где `a` и `b` — пользователи как списки `[id, name, email]`. Верните списком `[id, name, email]` **нового** пользователя `User`, взяв поля из `a`, но с `email = b.email`, если у `a` email **пустой**. Используйте `dataclasses.replace(User(*a), email=...)` или ручное создание.\n\n**Функция решения:**\n\n```python\ndef merge_users(a: list, b: list) -> list:\n    ...\n```",
            "examples": [
                {"input": "a = [1,'Ann',''], b = [2,'Bob','bb@x']", "output": "[1,'Ann','bb@x']", "explanation": "У a пустой email — берём из b."}
            ],
            "constraints": ["id:int; name,email:str"],
            "hints": [
                "email = b[2] if not a[2] else a[2].",
                "dataclasses.replace копирует объект без мутации исходного."
            ],
            "args": [
                [[1, "Ann", ""], [2, "Bob", "bb@x"]],
                [[1, "Ann", "a@b"], [2, "Bob", "bb@x"]],
                [[7, "I", ""], [8, "J", ""]],
                [[3, "C", "c@c"], [4, "D", "d@d"]],
                [[5, "E", ""], [6, "F", "f@f"]],
                [[0, "", "keep"], [9, "Z", "z@z"]]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])