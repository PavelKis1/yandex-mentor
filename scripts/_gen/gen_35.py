"""Данные блока 35: Type Hints (типизация)."""
from genlib import run

LECTURE_SLUG = "35_type_hints"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "35",
        "slug": "type-hints",
        "title": "Type Hints: коллекции, TypedDict, generics",
        "description": "Пишем типизированный код: аннотации коллекций, TypedDict для API-ответов и обобщённые функции с TypeVar.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Type Hints", "Typing"],
        "learningOutcomes": [
            "Аннотировать list/dict и Optional",
            "Описывать структуру словаря через TypedDict",
            "Писать обобщённые функции с TypeVar"
        ],
        "complexity": {
            "timeComplexity": "O(n) на задачи блока",
            "spaceComplexity": "O(n)",
            "explanation": "Типизация не меняет сложность алгоритма; задачи проверяют результат, а mypy отдельно."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что вернёт Optional[str] для отсутствующего значения?",
                "options": [
                    {"id": "opt1", "text": "None или строку", "isCorrect": True, "explanation": "Optional[str] == str | None."},
                    {"id": "opt2", "text": "Только строку", "isCorrect": False, "explanation": "Это str без None."},
                    {"id": "opt3", "text": "Список строк", "isCorrect": False, "explanation": "Это уже list[str]."}
                ],
                "hint": "Что означает Optional буквально?"
            },
            {
                "id": "q2",
                "question": "Чем TypedDict отличается от dict?",
                "options": [
                    {"id": "opt1", "text": "Задаёт структуру с типами полей", "isCorrect": True, "explanation": "TypedDict типизирует конкретные ключи словаря."},
                    {"id": "opt2", "text": "Это быстрый словарь", "isCorrect": False, "explanation": "Это только аннотация типов."},
                    {"id": "opt3", "text": "Это неизменяемый словарь", "isCorrect": False, "explanation": "Не про неизменяемость."}
                ],
                "hint": "Какие поля разрешены?"
            }
        ],
        "attachedTasks": [
            {"taskId": "35-p1", "title": "Группировка по первой букве", "difficulty": "easy", "slug": "group-by-first-letter"},
            {"taskId": "35-p2", "title": "TypedDict для API", "difficulty": "medium", "slug": "user-name"},
            {"taskId": "35-p3", "title": "Обобщённый first", "difficulty": "hard", "slug": "first-item"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Аннотируйте контейнеры: list[str], dict[str, list[str]].",
                "Optional[T] == T | None; используйте для возможно пустых значений.",
                "TypedDict описывает структуру словаря с типами полей.",
                "TypeVar('T') делает функцию обобщённой: Sequence[T] -> T."
            ]
        }
    },
    "problems": [
        {
            "id": "35-p1", "title": "Группировка по первой букве", "difficulty": "easy",
            "lecture_id": "35", "order": 1, "entry_function": "group_by_first_letter",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def group_by_first_letter(words: list[str]) -> dict[str, list[str]]:\n    \"\"\"Группировать слова по первой букве: {буква: [слова]}.\"\"\"\n    ...",
            "description": "Реализуйте типизированную `group_by_first_letter(words: list[str]) -> dict[str, list[str]]`, которая группирует слова по **первой букве** и возвращает словарь `{буква: [список слов в порядке появления]}`.\n\n**Функция решения:**\n\n```python\ndef group_by_first_letter(words: list[str]) -> dict[str, list[str]]:\n    ...\n```",
            "examples": [
                {"input": "words = ['apple','ant','banana']", "output": "{'a':['apple','ant'], 'b':['banana']}", "explanation": "Первая буква определяет группу."}
            ],
            "constraints": ["0 ≤ len(words) ≤ 10^4; слова непустые"],
            "hints": [
                "defaultdict(list) и w[0] как ключ.",
                "Сохранение порядка появления важно — верните dict(g)."
            ],
            "args": [
                [["apple", "ant", "banana"]],
                [[]],
                [["x"]],
                [["aa", "ab", "ba", "bb"]],
                [["zoo", "zap"]],
                [["m", "n", "m"]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "35-p2", "title": "TypedDict для API", "difficulty": "medium",
            "lecture_id": "35", "order": 2, "entry_function": "user_name",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "from typing import TypedDict\n\nclass UserResponse(TypedDict):\n    id: int\n    name: str\n    friends: list[int]\n\ndef user_name(usr: UserResponse) -> str:\n    \"\"\"Вернуть usr['name'].\"\"\"\n    ...",
            "description": "Опишите `TypedDict` `UserResponse` с полями `id: int`, `name: str`, `friends: list[int]`. Функция `user_name(usr)` принимает такой объект и возвращает `usr['name']`.\n\n**Функция решения:**\n\n```python\ndef user_name(usr: UserResponse) -> str:\n    ...\n```",
            "examples": [
                {"input": "{'id': 1, 'name': 'Ann', 'friends': [3, 7]}", "output": "'Ann'", "explanation": "Возвращаем поле name."}
            ],
            "constraints": ["usr — словарь вида UserResponse"],
            "hints": [
                "TypedDict задаёт структуру; доступ usr['name'].",
                "mypy подсветит передачу невалидного объекта."
            ],
            "args": [
                [{"id": 1, "name": "Ann", "friends": [3, 7]}],
                [{"id": 2, "name": "Bob", "friends": []}],
                [{"id": 3, "name": "", "friends": [1]}],
                [{"id": 4, "name": "Cid", "friends": [1, 2, 3]}],
                [{"id": 5, "name": "D", "friends": [9]}],
                [{"id": 6, "name": "Eve", "friends": [0, 0]}]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "35-p3", "title": "Обобщённый first", "difficulty": "hard",
            "lecture_id": "35", "order": 3, "entry_function": "first_item",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "from typing import TypeVar, Sequence\n\nT = TypeVar('T')\n\ndef first_item(items: Sequence[T]) -> T:\n    \"\"\"Первый элемент любой последовательности.\"\"\"\n    ...",
            "description": "Напишите **обобщённую** функцию `first_item(items: Sequence[T]) -> T` с `TypeVar`, возвращающую **первый элемент** последовательности (списка, кортежа или строки). Для пустой последовательности можете вернуть `None`.\n\n**Функция решения:**\n\n```python\ndef first_item(items: Sequence[T]) -> T:\n    ...\n```",
            "examples": [
                {"input": "items = [1, 2, 3]", "output": "1", "explanation": "Первый элемент списка."},
                {"input": "items = ('a', 'b')", "output": "'a'", "explanation": "Первый элемент кортежа."}
            ],
            "constraints": ["items — непустая последовательность"],
            "hints": [
                "return items[0].",
                "TypeVar связывает тип аргумента и возвращаемого значения."
            ],
            "args": [
                [[1, 2, 3]],
                [("a", "b")],
                ["hello"],
                [[7]],
                [(True,)],
                [[1.5, 2.5]]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])