"""Данные блока 48: Docker."""
from genlib import run

LECTURE_SLUG = "48_docker"

meta = {
    "lecture_slug": LECTURE_SLUG,
    "data": {
        "id": "48",
        "slug": "docker",
        "title": "Docker: контейнеры, образы, слои",
        "description": "Разбираем Docker: слои, ignore, теги.",
        "durationMinutes": 15,
        "difficulty": "junior",
        "tags": ["Docker", "Containers", "DevOps"],
        "learningOutcomes": ["Слои", "Ignore", "Теги"],
        "complexity": {"timeComplexity": "O(1)", "spaceComplexity": "O(1)", "explanation": "Базовые операции с Docker."},
        "quizzes": [],
        "attachedTasks": [
            {"taskId": "48-p1", "title": "Слои Dockerfile", "difficulty": "easy", "slug": "layer-count"},
            {"taskId": "48-p2", "title": "Docker ignore", "difficulty": "medium", "slug": "ignore-pattern"},
            {"taskId": "48-p3", "title": "Валидация тега", "difficulty": "hard", "slug": "tag-valid"}
        ],
        "cheatSheet": {"summary60Sec": ["RUN/COPY/ADD - слои", ".dockerignore - исключения", "Теги - буквы, цифры, ., -, _"]}
    },
    "problems": [
        {
            "id": "48-p1", "title": "Слои Dockerfile", "difficulty": "easy",
            "lecture_id": "48", "order": 1, "entry_function": "dockerfile_layer_count",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def dockerfile_layer_count(commands: list) -> int:\n    ...",
            "description": "Вернуть количество слоев (RUN, COPY, ADD).",
            "examples": [{"input": "dockerfile_layer_count(['RUN x', 'FROM y'])", "output": "1"}],
            "args": [[['RUN x', 'FROM y']], [['COPY x .', 'RUN z']]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "48-p2", "title": "Docker ignore", "difficulty": "medium",
            "lecture_id": "48", "order": 2, "entry_function": "docker_ignore_pattern",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def docker_ignore_pattern(file: str, patterns: list) -> bool:\n    ...",
            "description": "True, если файл попадает под паттерн.",
            "examples": [{"input": "docker_ignore_pattern('a.log', ['*.log'])", "output": "True"}],
            "args": [['a.log', ['*.log']], ['b.txt', ['*.log']]],
            "hidden": [False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        },
        {
            "id": "48-p3", "title": "Валидация тега", "difficulty": "hard",
            "lecture_id": "48", "order": 3, "entry_function": "image_tag_valid",
            "lecture_slug": LECTURE_SLUG,
            "starter_code": "def image_tag_valid(tag: str) -> bool:\n    ...",
            "description": "True, если тег валиден (a-z, 0-9, ., -, _).",
            "examples": [{"input": "image_tag_valid('v1.0')", "output": "True"}],
            "args": [["v1.0"], ["v1:0"], ["valid-tag"]],
            "hidden": [False, False, True],
            "constraints": "time: 1s, memory: 256mb",
            "hints": []
        }
    ]
}

if __name__ == "__main__":
    run([meta])
