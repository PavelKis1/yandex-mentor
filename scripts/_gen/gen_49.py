"""Данные блока 49: Docker Compose."""
from genlib import run

LECTURE_SLUG = "49_docker_compose"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "49",
        "slug": "docker_compose",
        "title": "Docker Compose: оркестрация",
        "description": "Разбираем Compose: зависимости, сети, объемы.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Docker", "Compose", "Orchestration"],
        "learningOutcomes": ["Зависимости", "Сети", "Объемы"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции с Compose."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "49-p1", "title": "Зависимости сервисов", "difficulty": "easy", "slug": "service-deps"},
            {"taskId": "49-p2", "title": "Режим сети", "difficulty": "medium", "slug": "network-mode"},
            {"taskId": "49-p3", "title": "Маппинг объемов", "difficulty": "hard", "slug": "volume-mapping"}
        ],
        "cheatSheet": {"summary60Sec": ["depends_on для порядка", "network_mode для сети", "volume: host:container"]}
    },
    "problems": [
        {
            "id": "49-p1", "title": "Зависимости сервисов", "difficulty": "easy",
            "lecture_id": "49", "order": 1, "entry_function": "compose_service_dependency",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def compose_service_dependency(services: dict) -> list:\n    ...",
            "description": "Вернуть список сервисов в порядке запуска.",
            "examples": [{"input": "compose_service_dependency({'a': {'depends_on': ['b']}, 'b': {}})", "output": "['b', 'a']"}],
            "args": [[{'a': {'depends_on': ['b']}, 'b': {}}], [{'a': {}}]],
            "hidden": [True, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "49-p2", "title": "Режим сети", "difficulty": "medium",
            "lecture_id": "49", "order": 2, "entry_function": "compose_network_mode",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def compose_network_mode(config: dict) -> str:\n    ...",
            "description": "Вернуть режим сети (bridge по умолчанию).",
            "examples": [{"input": "compose_network_mode({'network_mode': 'host'})", "output": "'host'"}],
            "args": [[{'network_mode': 'host'}], [{}]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "49-p3", "title": "Маппинг объемов", "difficulty": "hard",
            "lecture_id": "49", "order": 3, "entry_function": "compose_volume_mapping",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def compose_volume_mapping(mapping: str) -> bool:\n    ...",
            "description": "True, если это корректный маппинг.",
            "examples": [{"input": "compose_volume_mapping('./data:/data')", "output": "True"}],
            "args": [['./data:/data'], ['invalid']],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
