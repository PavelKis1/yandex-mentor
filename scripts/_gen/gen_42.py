"""Данные блока 42: Транзакции и ACID (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "42_transactions"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "42",
        "slug": "transactions",
        "title": "Транзакции и ACID: атомарность, откат, уровни изоляции",
        "description": "Транзакции гарантируют согласованность данных. Учимся атомарному переводу средств, откату при ошибке и выбору уровня изоляции против аномалий.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["SQL", "ACID", "Transaction", "Isolation"],
        "learningOutcomes": [
            "Проводить атомарный перевод между счетами",
            "Моделировать COMMIT/ROLLBACK операций",
            "Подбирать уровень изоляции под аномалию"
        ],
        "complexity": {
            "timeComplexity": "O(n) на задачи блока",
            "spaceComplexity": "O(1)–O(n)",
            "explanation": "Задачи проверяют семантику транзакций на простых числовых состояниях."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что делает ROLLBACK при ошибке в середине транзакции?",
                "options": [
                    {"id": "opt1", "text": "Отменяет все изменения транзакции", "isCorrect": True, "explanation": "Состояние возвращается к началу транзакции."},
                    {"id": "opt2", "text": "Отменяет только последнюю команду", "isCorrect": False, "explanation": "ROLLBACK откатывает всю транзакцию."},
                    {"id": "opt3", "text": "Коммитит успешные команды", "isCorrect": False, "explanation": "Это противоречит атомарности."}
                ],
                "hint": "Атомарность = всё или ничего."
            },
            {
                "id": "q2",
                "question": "Какой уровень изоляции защищает от всех аномалий?",
                "options": [
                    {"id": "opt1", "text": "SERIALIZABLE", "isCorrect": True, "explanation": "Эффект «как будто последовательно»."},
                    {"id": "opt2", "text": "READ COMMITTED", "isCorrect": False, "explanation": "Не мешает non-repeatable read."},
                    {"id": "opt3", "text": "READ UNCOMMITTED", "isCorrect": False, "explanation": "Допускает даже dirty reads."}
                ],
                "hint": "Максимальная гарантия — про serializable."
            }
        ],
        "attachedTasks": [
            {"taskId": "42-p1", "title": "Атомарный перевод", "difficulty": "easy", "slug": "atomic-transfer"},
            {"taskId": "42-p2", "title": "COMMIT / ROLLBACK", "difficulty": "medium", "slug": "commit-rollback"},
            {"taskId": "42-p3", "title": "Уровни изоляции", "difficulty": "hard", "slug": "isolation-levels"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "Транзакция атомарна: или все изменения, или ни одного.",
                "При ошибке ROLLBACK возвращает состояние к началу.",
                "READ COMMITTED борется с dirty reads.",
                "SERIALIZABLE защищает от всех аномалий чтения."
            ]
        }
    },
    "problems": [
{
            "id": "42-p1", "title": "Атомарный перевод", "difficulty": "easy",
            "lecture_id": "42", "order": 1, "entry_function": "transfer_balances",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def transfer_balances(state: list[int], from_id: int, to_id: int, amount: int):\n    \"\"\"Атомарно перевести amount между счётами state; None при нехватке средств.\"\"\"\n    ...",
            "description": "Список `state` хранит балансы счетов. Реализуйте **атомарный перевод** `transfer_balances(state, from_id, to_id, amount)`:\n- если на счёте `from_id` достаточно средств — списать `amount` и зачислить на `to_id`, вернуть новый список балансов;\n- если средств не хватает — перевод не выполняется, верните `None` (транзакция отменена).\n\nВажно: ни один счёт не должен измениться при неудачном переводе.\n\n**Функция решения:**\n\n```python\ndef transfer_balances(state: list[int], from_id: int, to_id: int, amount: int):\n    ...\n```",
            "examples": [
                {"input": "transfer_balances([100, 0], 0, 1, 10)", "output": "[90, 10]", "explanation": "10 переведено с 1-го на 2-й счет."},
                {"input": "transfer_balances([10, 0], 0, 1, 20)", "output": "None", "explanation": "Недостаточно средств — транзакция отменена."}
            ],
            "constraints": ["0 ≤ from_id, to_id < len(state)", "amount ≥ 0"],
            "hints": [
                "Сначала проверьте остаток, потом переводите.",
                "Возвращайте новый список, а не мутируйте входной."
            ],
            "args": [
                [[100, 0], 0, 1, 10],
                [[100, 50, 0], 1, 2, 5],
                [[10, 0], 0, 1, 20],
                [[0, 100], 1, 0, 100],
                [[50, 10], 0, 1, 60],
                [[33, 33, 33], 0, 2, 33]
            ],
            "hidden": [False, False, False, True, True, True]
        },
{
            "id": "42-p2", "title": "COMMIT / ROLLBACK", "difficulty": "medium",
            "lecture_id": "42", "order": 2, "entry_function": "transaction_commit_or_rollback",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def transaction_commit_or_rollback(state: list[int], ops: list[list]) -> list[int]:\n    \"\"\"Применить операции; при op=['fail'] вернуть исходное состояние (ROLLBACK).\"\"\"\n    ...",
            "description": "Список `ops` описывает команды внутри транзакции, `state` — текущий баланс счетов.\n- `['add', i, n]` — увеличить счёт `i` на `n`;\n- `['sub', i, n]` — уменьшить счёт `i` на `n`;\n- `['fail']` — транзакция прерывается ошибкой, происходит **ROLLBACK** — возвращаем исходное состояние без изменений.\n\nЕсли ошибок нет — применяем все команды и **COMMIT**: возвращаем итоговое состояние.\n\n**Функция решения:**\n\n```python\ndef transaction_commit_or_rollback(state: list[int], ops: list[list]) -> list[int]:\n    ...\n```",
            "examples": [
                {"input": "transaction_commit_or_rollback([100, 0], [['add',0,50],['add',1,50]])", "output": "[150, 50]", "explanation": "Все команды успешны — COMMIT."},
                {"input": "transaction_commit_or_rollback([100, 0], [['add',0,50],['fail'],['add',1,50]])", "output": "[100, 0]", "explanation": "Ошибка — ROLLBACK до исходного состояния."}
            ],
            "constraints": ["Команды корректны по индексам", "n ≥ 0"],
            "hints": [
                "Сохраните копию исходного состояния.",
                "При ['fail'] верните эту копию немедленно."
            ],
            "args": [
                [[100, 0], [["add", 0, 50], ["add", 1, 50]]],
                [[100, 0], [["add", 0, 50], ["fail"], ["sub", 1, 20]]],
                [[10, 10, 10], [["add", 2, 5], ["sub", 0, 3]]],
                [[5, 5], [["fail"]]],
                [[1, 2, 3], [["add", 1, 4], ["sub", 2, 2], ["add", 0, 1]]],
                [[100, 100], [["add", 0, 1], ["fail"], ["add", 0, 1]]]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "42-p3", "title": "Уровни изоляции", "difficulty": "hard",
            "lecture_id": "42", "order": 3, "entry_function": "isolation_prevents",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def isolation_prevents(level: str, anomaly: str) -> bool:\n    \"\"\"True, если уровень изоляции level предотвращает аномалию anomaly.\"\"\"\n    ...",
            "description": "Верните `True`, если уровень изоляции `level` предотвращает аномалию `anomaly`. Используйте таблицу соответствий:\n\n- `read_uncommitted`: не предотвращает ни одной из аномалий;\n- `read_committed`: только `dirty_read`;\n- `repeatable_read`: `dirty_read`, `non_repeatable_read`, `lost_update`;\n- `serializable`: `dirty_read`, `non_repeatable_read`, `lost_update`, `phantom_read`.\n\nДопустимые аномалии: `dirty_read`, `lost_update`, `non_repeatable_read`, `phantom_read`.\n\n**Функция решения:**\n\n```python\ndef isolation_prevents(level: str, anomaly: str) -> bool:\n    ...\n```",
            "examples": [
                {"input": "isolation_prevents('serializable', 'phantom_read')", "output": "True", "explanation": "Serializable защищает от всех аномалий."},
                {"input": "isolation_prevents('read_committed', 'non_repeatable_read')", "output": "False", "explanation": "Read committed видит повторные изменения."}
            ],
            "constraints": ["level в списке четырёх уровней", "anomaly в списке аномалий"],
            "hints": [
                "Составьте словарь уровень → множество допустимых аномалий.",
                "Чем выше изоляция, тем больше защита."
            ],
            "args": [
                ["serializable", "phantom_read"],
                ["read_committed", "dirty_read"],
                ["repeatable_read", "phantom_read"],
                ["read_uncommitted", "dirty_read"],
                ["repeatable_read", "lost_update"],
                ["read_committed", "non_repeatable_read"]
            ],
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])