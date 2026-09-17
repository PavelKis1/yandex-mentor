"""Данные блока 43: Redis как in-memory key-value store (детерминированная проверка)."""
from genlib import run

LECTURE_SLUG = "43_redis"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "43",
        "slug": "redis",
        "title": "Redis: ключ-значение, счётчики, TTL и LRU-кэш",
        "description": "Redis хранит данные в памяти: счётчики с атомарным INCR, значения с TTL и вытеснение по LRU. Моделируем эти поведенческие правила функциями.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Redis", "Cache", "TTL", "LRU", "Key-Value"],
        "learningOutcomes": [
            "Моделировать атомарный INCR-счётчик",
            "Читать значение с учётом TTL",
            "Выбирать ключ для вытеснения по LRU"
        ],
        "complexity": {
            "timeComplexity": "O(1)–O(k) на задачи блока",
            "spaceComplexity": "O(n)",
            "explanation": "Задачи воспроизводят семантику команд Redis без реального сервера."
        },
        "quizzes": [
            {
                "id": "q1",
                "question": "Что возвращает INCR для отсутствующего ключа?",
                "options": [
                    {"id": "opt1", "text": "1 (ключ создаётся со значением 0)", "isCorrect": True, "explanation": "INCR несуществующего ключа даёт 1."},
                    {"id": "opt2", "text": "Ошибку", "isCorrect": False, "explanation": "Redis создаёт ключ автоматически."},
                    {"id": "opt3", "text": "0", "isCorrect": False, "explanation": "0 было бы до счётчика, но INCR вернёт 1."}
                ],
                "hint": "Какое значение получится, если 0 увеличить на 1?"
            },
            {
                "id": "q2",
                "question": "Какой ключ вытесняется при LRU?",
                "options": [
                    {"id": "opt1", "text": "Давно не использовавшийся", "isCorrect": True, "explanation": "Least Recently Used — старший по давности."},
                    {"id": "opt2", "text": "Самый маленький по размеру", "isCorrect": False, "explanation": "Это больше про размер, не про LRU."},
                    {"id": "opt3", "text": "Самый новый", "isCorrect": False, "explanation": "Новые живут дольше."}
                ],
                "hint": "Что значит буква L в LRU?"
            }
        ],
        "attachedTasks": [
            {"taskId": "43-p1", "title": "INCR-счётчик", "difficulty": "easy", "slug": "redis-incr"},
            {"taskId": "43-p2", "title": "Значение по TTL", "difficulty": "medium", "slug": "cache-ttl"},
            {"taskId": "43-p3", "title": "LRU-вытеснение", "difficulty": "hard", "slug": "lru-eviction"}
        ],
        "cheatSheet": {
            "summary60Sec": [
                "INCR key атомарно увеличивает счётчик, создавая его с 0.",
                "Записи SET EX ставят expires_at; истёкшие ключи возвращают NULL.",
                "LRU вытесняет ключ с самым старым временем последнего обращения.",
                "Redis хранит данные в памяти — отсюда скорость."
            ]
        }
    },
    "problems": [
{
            "id": "43-p1", "title": "INCR-счётчик", "difficulty": "easy",
            "lecture_id": "43", "order": 1, "entry_function": "redis_incr",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def redis_incr(store: dict, key: str) -> int:\n    \"\"\"Атомарно увеличить счётчик key на 1; вернуть новое значение.\"\"\"\n    ...",
            "description": "Команда Redis `INCR key` атомарно увеличивает целочисленное значение по ключу на `1`. Если ключа нет — он создаётся со значением `0`, после чего инкрементируется до `1`.\n\nРеализуйте `redis_incr(store, key)`, возвращающую **новое значение** счётчика (не мутируя переданный `store`): для отсутствующего ключа верните `1`, иначе — текущее значение плюс `1`.\n\n**Функция решения:**\n\n```python\ndef redis_incr(store: dict, key: str) -> int:\n    ...\n```",
            "examples": [
                {"input": "redis_incr({}, 'hits')", "output": "1", "explanation": "Ключа не было — создаётся и инкрементируется."},
                {"input": "redis_incr({'hits': 5}, 'hits')", "output": "6", "explanation": "Существующий счётчик 5 + 1."}
            ],
            "constraints": ["store — словарь целых значений"],
            "hints": [
                "store.get(key, 0) вернёт 0 для отсутствующего ключа.",
                "Верните store.get(key, 0) + 1."
            ],
            "args": [
                [{}, "hits"],
                [{"hits": 5}, "hits"],
                [{"views": 0}, "views"],
                [{"v": 10}, "other"],
                [{"a": -1}, "a"],
                [{}, "x"]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "43-p2", "title": "Значение по TTL", "difficulty": "medium",
            "lecture_id": "43", "order": 2, "entry_function": "cache_get",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def cache_get(store: dict, key: str, now: int):\n    \"\"\"Вернуть значение ключа, если он не истёк (now <= expires_at), иначе None.\"\"\"\n    ...",
            "description": "Записи кэша хранят `{'value': ..., 'expires_at': ...}` (метка времени истечения). Реализуйте `cache_get(store, key, now)`:\n- если ключа нет или момент `now` **больше** `expires_at` (TTL истёк) — верните `None`;\n- если `now <= expires_at` — верните `value`.\n\n**Функция решения:**\n\n```python\ndef cache_get(store: dict, key: str, now: int):\n    ...\n```",
            "examples": [
                {"input": "cache_get({'a': {'value': 10, 'expires_at': 100}}, 'a', 50)", "output": "10", "explanation": "Рано — значение живо."},
                {"input": "cache_get({'a': {'value': 10, 'expires_at': 100}}, 'a', 101)", "output": "None", "explanation": "Момент истёк — ключ недоступен."}
            ],
            "constraints": ["expires_at и now — целые метки времени"],
            "hints": [
                "Проверьте наличие ключа через `key not in store`.",
                "Истёк, когда now > expires_at."
            ],
            "args": [
                [{"a": {"value": 10, "expires_at": 100}}, "a", 50],
                [{"a": {"value": 10, "expires_at": 100}}, "a", 100],
                [{"a": {"value": 10, "expires_at": 100}}, "a", 101],
                [{"x": {"value": "ok", "expires_at": 5}}, "x", 5],
                [{}, "missing", 0],
                [{"b": {"value": 7, "expires_at": 1}}, "b", 9]
            ],
            "hidden": [False, False, False, True, True, True]
        },
        {
            "id": "43-p3", "title": "LRU-вытеснение", "difficulty": "hard",
            "lecture_id": "43", "order": 3, "entry_function": "lru_evict_key",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def lru_evict_key(last_used: dict, capacity: int):\n    \"\"\"Если ключей больше capacity — вернуть ключ с самым старым last_used, иначе None.\"\"\"\n    ...",
            "description": "Словарь `last_used` хранит `ключ → время последнего обращения`. При превышении ёмкости `capacity` кэш вытесняет **наиболее давно использованный (LRU)** ключ.\n\nРеализуйте `lru_evict_key(last_used, capacity)`:\n- если `len(last_used) <= capacity` — вытеснение не нужно, верните `None`;\n- иначе верните ключ с **минимальным** временем последнего обращения.\n\n**Функция решения:**\n\n```python\ndef lru_evict_key(last_used: dict, capacity: int):\n    ...\n```",
            "examples": [
                {"input": "lru_evict_key({'a': 10, 'b': 5}, 1)", "output": "'b'", "explanation": "b обращались раньше (5 < 10)."},
                {"input": "lru_evict_key({'a': 10, 'b': 5}, 3)", "output": "None", "explanation": "Места достаточно — вытеснять нечего."}
            ],
            "constraints": ["capacity ≥ 0", "last_used непуст"],
            "hints": [
                "min(last_used, key=last_used.get) даёт самый старый ключ.",
                "Сначала сравните размер с capacity."
            ],
            "args": [
                [{"a": 10, "b": 5}, 1],
                [{"a": 10, "b": 5, "c": 3}, 2],
                [{"a": 10, "b": 5}, 3],
                [{"x": 1, "y": 2}, 1],
                [{"p": 9, "q": 8, "r": 7, "s": 6}, 2],
                [{"a": 1}, 2]
            ],
            "hidden": [False, False, False, True, True, True]
        }
    ]
}

if __name__ == "__main__":
    run([meta])