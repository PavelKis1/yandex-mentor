"""Данные блока 33: Context Managers (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "33_context_managers"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "33",
        "slug": "context-managers",
        "title": "Context Managers: файлы, таймеры, подавление ошибок",
        "description": "Контекстные менеджеры гарантируют очистку ресурсов. Проверяем их по детерминированному эффекту: корректный выход, счётчики, подавление исключений.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Python", "Context Managers", "with"],
        "learningOutcomes": [
            "Строить контекстный менеджер через __enter__/__exit__",
            "Использовать @contextmanager с yield",
            "Подавлять исключения возвратом True из __exit__"
        ],
        "complexity": {
            "timeComplexity": "O(n) на задачи блока",
            "spaceComplexity": "O(1) дополнительно",
            "explanation": "Контекстные менеджеры добавляют работу при входе/выходе из блока with."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что делает __exit__ при возврате True?",
                "options": [
                    {"id": "opt1", "text": "Подавляет возникшее исключение", "isCorrect": True, "explanation": "True означает «исключение обработано, бросать не надо»."},
                    {"id": "opt2", "text": "Закрывает файл", "isCorrect": False, "explanation": "Закрытие файла — следствие кода в __exit__, не само по себе."},
                    {"id": "opt3", "text": "Вызывает исключение повторно", "isCorrect": False, "explanation": "Противоположно: True именно гасит его."}
                ],
                "hint": "Какое значение гасит ошибку?"
            },
            {
                "id": "q2",
                "question": "Зачем with вместо try/finally?",
                "options": [
                    {"id": "opt1", "text": "Короче и гарантирует очистку", "isCorrect": True, "explanation": "with всегда вызывает __exit__, даже при исключении."},
                    {"id": "opt2", "text": "Быстрее try/finally", "isCorrect": False, "explanation": "Скорость не главное."},
                    {"id": "opt3", "text": "Это единственный способ открыть файл", "isCorrect": False, "explanation": "Файл можно открыть и без with, но тогда надо закрывать вручную."}
                ],
                "hint": "Кто гарантирует закрытие?"
            }
        ],
        "attachedTasks": [
            {"taskId": "33-p1", "title": "Число строк (менеджер файла)", "difficulty": "easy", "slug": "write-lines"},
            {"taskId": "33-p2", "title": "Действие при выходе", "difficulty": "medium", "slug": "append-on-exit"},
            {"taskId": "33-p3", "title": "Подавление ValueError", "difficulty": "hard", "slug": "suppress-sum"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "with гарантирует вызов __exit__ даже при ошибке.",
                "@contextmanager оборачивает генератор вокруг yield.",
                "__exit__, возвращающий True, подавляет исключение.",
                "Ресурсы (файлы, соединения) закрываются автоматически."
            ]
        }
    },
    "problems": [
        {
            "id": "33-p1", "title": "Число строк (менеджер файла)", "difficulty": "easy",
            "lecture_id": "33", "order": 1, "entry_function": "write_lines",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def open_file(path, mode):\n    \"\"\"Контекстный менеджер, гарантирующий закрытие файла.\"\"\"\n    ...\n\ndef write_lines(items: list[str]) -> int:\n    \"\"\"Записать items во временный файл через with open_file и вернуть число строк.\"\"\"\n    ...",
            "description": "Реализуйте контекстный менеджер `open_file(path, mode)` с `__enter__`/`__exit__`, который **гарантирует закрытие файла**. Используя его в `with`, функция `write_lines(items)` записывает строки `items` во временный файл и возвращает их **количество** (`len(items)`).\n\n**Функция решения:**\n\n```python\ndef write_lines(items: list[str]) -> int:\n    ...\n```",
            "examples": [
                {"input": "items = ['a','b']", "output": "2", "explanation": "Менеджер записал 2 строки и закрыл файл."},
                {"input": "items = []", "output": "0", "explanation": "Строк не было."}
            ],
            "constraints": ["0 ≤ len(items) ≤ 10^4"],
            "hints": [
                "__enter__ возвращает открытый файл, __exit__ вызывает f.close().",
                "Верните len(items) — менеджер отработал корректно."
            ],
            "args": [
                [["a", "b"]],
                [[]],
                [["x"]],
                [["1", "2", "3"]],
                [["hello", "world"]],
                [["a", "a", "a"]]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "33-p2", "title": "Действие при выходе", "difficulty": "medium",
            "lecture_id": "33", "order": 2, "entry_function": "append_on_exit",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "class AppendOnExit:\n    \"\"\"КМ: при выходе из with добавляет value в список.\"\"\"\n    ...\n\ndef append_on_exit(value, base):\n    \"\"\"Вернуть список, к которому контекстный менеджер добавит value при ВЫХОДЕ.\"\"\"\n    ...",
            "description": "Напишите контекстный менеджер, который при **выходе** из `with` добавляет `value` в список. Функция `append_on_exit(value, base)` создаёт список `[base]`, использует менеджер в `with` и возвращает итоговый список `[base, value]` (доказательство того, что код в `__exit__` выполнился).\n\n**Функция решения:**\n\n```python\ndef append_on_exit(value, base):\n    ...\n```",
            "examples": [
                {"input": "value = 3, base = 0", "output": "[0, 3]", "explanation": "На выходе значение добавилось в список."}
            ],
            "constraints": ["Любые значения value, base"],
            "hints": [
                "__enter__ может вернуть список; код в __exit__ выполняет lst.append(value).",
                "Используйте with менеджер вокруг строки, чтобы вызвался __exit__."
            ],
            "args": [
                [3, 0],
                ["x", "y"],
                [5, 5],
                [10, 1],
                ["end", "start"],
                [9, 8]
            ],
            "hidden": [False, False, True, True, True, True]
        },
        {
            "id": "33-p3", "title": "Подавление ValueError", "difficulty": "hard",
            "lecture_id": "33", "order": 3, "entry_function": "suppress_sum",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "class suppress:\n    \"\"\"КМ, подавляющий указанное исключение внутри блока with.\"\"\"\n    ...\n\ndef suppress_sum(items: list) -> int:\n    \"\"\"Сумма int(x) по items, игнорируя элементы, не парсящиеся в int (через свой suppress).\"\"\"\n    ...",
            "description": "Реализуйте контекстный менеджер `suppress(Exc)`, у которого `__exit__` возвращает `True` при совпадении с исключением `Exc` (подавление). Функция `suppress_sum(items)` проходит по элементам, вычисляет `int(x)` **внутри** `with suppress(ValueError)` и суммирует успешно распарсенные значения.\n\n**Функция решения:**\n\n```python\ndef suppress_sum(items: list) -> int:\n    ...\n```",
            "examples": [
                {"input": "items = ['1', 'abc', '2']", "output": "3", "explanation": "'abc' не парсится — ValueError подавлен."},
                {"input": "items = []", "output": "0", "explanation": "Пустой список."}
            ],
            "constraints": ["0 ≤ len(items) ≤ 10^5"],
            "hints": [
                "__exit__ возвращает issubclass(exc, Exc).",
                "Внутри with выполняйте x = int(item); при подавлении переход к следующему."
            ],
            "args": [
                [["1", "abc", "2"]],
                [[]],
                [["a"]],
                [["5", "5"]],
                [["0", "x", "x", "3"]],
                [["10", "20"]]
            ],
            "hidden": [False, False, True, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])