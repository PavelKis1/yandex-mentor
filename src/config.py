"""Настройки и пути проекта.

Вся работа с файлами идёт через этот модуль, чтобы пути были в одном месте:
- backend/            — контент учебного плана (не изменяется сервером)
- backend/roadmap.json   — порядок разделов и тем
- backend/tasks/      — каталог задач: {NN_slug}/lecture.md + problems/pN.json
- data/               — динамические данные (progress, сохранённые решения)
- logs/               — файлы логов
"""
from pathlib import Path

# Корень репозитория (каталог, в котором лежат backend/, frontend/, server.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Контент учебного плана
CONTENT_DIR = BASE_DIR / "backend"
TASKS_DIR = CONTENT_DIR / "tasks"
ROADMAP_FILE = CONTENT_DIR / "roadmap.json"

# Динамические данные
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

PROGRESS_FILE = DATA_DIR / "progress.json"
ERRORS_FILE = DATA_DIR / "errors.json"
SOLUTIONS_DIR = DATA_DIR / "solutions"

HOST = "0.0.0.0"
PORT = 8000

# Безопасность
AUTH_USER = "admin"
AUTH_PASS = "admin" # ВАЖНО: смените пароль!
