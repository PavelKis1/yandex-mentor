"""Данные блока 44: HTTP — статусы, методы, условные запросы (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "44_http"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "44",
        "slug": "http",
        "title": "HTTP: коды ответа, безопасные методы и условные запросы",
        "description": "HTTP — язык общения клиента и сервера. Разбираем семантику кодов статуса, безопасные/идемпотентные методы и проверку ETag через If-None-Match.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["HTTP", "Status Codes", "REST", "ETag", "Cache"],
        "learningOutcomes": [
            "Сопоставлять ситуацию правильному коду статуса",
            "Различать безопасные и изменяющие методы",
            "Реализовывать условный ответ через ETag"
        ],
        "complexity": {
            "timeComplexity": "O(1) на задачи блока",
            "spaceComplexity": "O(1)",
            "explanation": "Задачи проверяют табличные знания HTTP и простые условия."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Какой код возвращается, когда ресурс не найден?",
                "options": [
                    {"id": "opt1", "text": "404 Not Found", "isCorrect": True, "explanation": "Ресурс отсутствует."},
                    {"id": "opt2", "text": "403 Forbidden", "isCorrect": False, "explanation": "Доступ запрещён, но ресурс есть."},
                    {"id": "opt3", "text": "500", "isCorrect": False, "explanation": "Это ошибка сервера."}
                ],
                "hint": "Клиент не нашёл ресурс по URL."
            },
            {
                "id": "q2",
                "question": "Кто такие «безопасные» методы HTTP?",
                "options": [
                    {"id": "opt1", "text": "Не изменяют состояние на сервере (GET, HEAD, OPTIONS)", "isCorrect": True, "explanation": "Безопасные — только чтение."},
                    {"id": "opt2", "text": "Все методы, включая POST", "isCorrect": False, "explanation": "POST изменяет данные."},
                    {"id": "opt3", "text": "Только DELETE", "isCorrect": False, "explanation": "DELETE удаляет ресурс."}
                ],
                "hint": "Безопасный = только чтение."
            }
        ],
        "attachedTasks": [
            {"taskId": "44-p1", "title": "Код статуса", "difficulty": "easy", "slug": "status-codes"},
            {"taskId": "44-p2", "title": "Разрешён ли метод", "difficulty": "medium", "slug": "method-allowed"},
            {"taskId": "44-p3", "title": "Условный запрос ETag", "difficulty": "hard", "slug": "etag-match"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "4xx — ошибка клиента, 5xx — ошибка сервера.",
                "GET/HEAD/OPTIONS безопасны, остальные меняют состояние.",
                "If-None-Match + ETag даёт 304, если клиент уже актуален.",
                "Символ '*' в If-None-Match означает «любой ETag»."
            ]
        }
    },
    "problems": [
{
            "id": "44-p1", "title": "Код статуса", "difficulty": "easy",
            "lecture_id": "44", "order": 1, "entry_function": "status_for",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def status_for(situation: str) -> int:\n    \"\"\"Вернуть HTTP-код по имени ситуации (см. таблицу).\"\"\"\n    ...",
            "description": "Верните корректный HTTP-код статуса по имени ситуации по таблице:\n\n- `ok` → 200, `created` → 201, `accepted` → 202, `no_content` → 204, `not_modified` → 304;\n- `bad_request` → 400, `unauthorized` → 401, `forbidden` → 403, `not_found` → 404, `not_allowed` → 405, `conflict` → 409, `gone` → 410, `validation` → 422;\n- `server_error` → 500, `unavailable` → 503.\n\n**Функция решения:**\n\n```python\ndef status_for(situation: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "status_for('not_found')", "output": "404", "explanation": "Ресурс не найден."},
                {"input": "status_for('created')", "output": "201", "explanation": "Ресурс успешно создан."}
            ],
            "constraints": ["situation — строка из таблицы"],
            "hints": [
                "Заведите словарь ситуация → код.",
                "Запомните группы: 2xx успех, 4xx клиент, 5xx сервер."
            ],
            "args": [["not_found"], ["created"], ["forbidden"], ["validation"]],
            "hidden": [False, False, False, True]
        },
        {
            "id": "44-p2", "title": "Разрешён ли метод", "difficulty": "medium",
            "lecture_id": "44", "order": 2, "entry_function": "method_allowed",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def method_allowed(method: str, read_only: bool) -> bool:\n    \"\"\"True, если метод разрешён: безопасные всегда, изменяющие — только если не read_only.\"\"\"\n    ...",
            "description": "Некоторые ресурсы доступны только для чтения. Реализуйте `method_allowed(method, read_only)`:\n- безопасные методы `GET`, `HEAD`, `OPTIONS` разрешены всегда (регистр не важен);\n- изменяющие методы (`POST`, `PUT`, `PATCH`, `DELETE`) — только если ресурс **не** `read_only`.\n\n**Функция решения:**\n\n```python\ndef method_allowed(method: str, read_only: bool) -> bool:\n    ...\n```",
            "examples": [
                {"input": "method_allowed('GET', True)", "output": "True", "explanation": "GET безопасен — разрешён даже для чтения."},
                {"input": "method_allowed('POST', True)", "output": "False", "explanation": "POST меняет состояние, а ресурс доступен только для чтения."}
            ],
            "constraints": ["method — непустая строка"],
            "hints": [
                "Приведите method.upper() и проверьте безопасное множество.",
                "Иначе верните not read_only."
            ],
            "args": [
                ["GET", False],
                ["GET", True],
                ["POST", False],
                ["POST", True],
                ["DELETE", True],
                ["HEAD", True]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "44-p3", "title": "Условный запрос ETag", "difficulty": "hard",
            "lecture_id": "44", "order": 3, "entry_function": "etag_match",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def etag_match(etag, if_none_match):\n    \"\"\"True, если клиент актуален (вернуть 304); '*' значит любой ETag.\"\"\"\n    ...",
            "description": "Условные запросы экономят трафик. Реализуйте `etag_match(etag, if_none_match)` — решает, вернуть ли серверу `304 Not Modified` (если состояние клиента актуально):\n- если `if_none_match` равен `None` — нет условия, верните `False`;\n- если `if_none_match == '*'` — клиент совпадает с любым вариантом, верните `True`;\n- иначе верните `etag == if_none_match`.\n\n**Функция решения:**\n\n```python\ndef etag_match(etag, if_none_match):\n    ...\n```",
            "examples": [
                {"input": "etag_match('\"abc\"', '\"abc\"')", "output": "True", "explanation": "ETag совпадает — клиент актуален, 304."},
                {"input": "etag_match('anything', '*')", "output": "True", "explanation": "Звёздочка принимает любой ETag."},
                {"input": "etag_match('\"abc\"', None)", "output": "False", "explanation": "Условия нет — отвечаем полным телом."}
            ],
            "constraints": ["etag может быть None или строкой", "if_none_match — строка или None"],
            "hints": [
                "Обработайте None раньше всего.",
                "'*' — шаблон «любое значение»."
            ],
            "args": [
                ["\"abc\"", "\"abc\""],
                ["\"abc\"", "\"xyz\""],
                ["anything", "*"],
                ["\"abc\"", None],
                [None, None],
                ["\"v1\"", "\"v2\""]
            ],
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])