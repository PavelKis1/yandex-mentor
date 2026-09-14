"""Хелперы работы с JSON-файлами и каталогами data/."""
import json
import os
import shutil
from pathlib import Path

from src import config


def atomic_write(path: Path, content: str) -> None:
    """Атомарная запись текста: temp-файл + os.replace (без частичных чтений)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(content, encoding="utf-8")
    os.replace(temp, path)


def ensure_dirs() -> None:
    """Создаёт каталоги data/, logs/ и data/solutions/, если их нет."""
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)


def migrate_legacy_files() -> None:
    """Одноразовый перенос старых файлов из корня (progress.json, errors.json)."""
    legacy = {
        "progress.json": config.PROGRESS_FILE,
        "errors.json": config.ERRORS_FILE,
    }
    for name, destination in legacy.items():
        source = config.BASE_DIR / name
        if source.exists() and not destination.exists():
            shutil.move(str(source), str(destination))

    for log_file in config.BASE_DIR.glob("*.log"):
        target = config.LOG_DIR / log_file.name
        if not target.exists():
            shutil.move(str(log_file), str(target))


def ensure_storage() -> None:
    """Готовит каталоги данных и переносит устаревшие файлы."""
    ensure_dirs()
    migrate_legacy_files()


def read_json(path: Path, default=None):
    """Прочитать JSON-файл; при отсутствии/ошибке вернуть default."""
    if not path.exists():
        return dict(default) if default is not None else {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return dict(default) if default is not None else {}


def write_json(path: Path, data) -> None:
    """Записать JSON-файл (utf-8, отступ 2, атомарно)."""
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2))


# === Сохранённые решения ===


def solution_path(problem_id: str) -> Path:
    """Путь к файлу с сохранённым решением пользователя: data/solutions/{id}.py."""
    return config.SOLUTIONS_DIR / f"{problem_id}.py"


def read_solution(problem_id: str) -> str | None:
    """Сохранённое решение (None, если ещё не отправлялось)."""
    path = solution_path(problem_id)
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None
    return None


def save_solution(problem_id: str, code: str) -> None:
    """Сохранить решение (перезаписывая прошлое) атомарно."""
    atomic_write(solution_path(problem_id), code)