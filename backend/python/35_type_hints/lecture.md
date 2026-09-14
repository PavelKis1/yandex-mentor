# Лекция: 35 — Статическая типизация (Type Hints) и Mypy

## Обзор темы
Аннотации типов в Python (PEP 484 и последующие) позволяют использовать статическую типизацию, улучшая читаемость кода, упрощая рефакторинг и позволяя находить ошибки типов на этапе статического анализа до запуска приложения.

---

## Подробный теоретический минимум

### 1. Базовые и составные типы
- **Примитивы**: `int`, `str`, `float`, `bool`, `bytes`.
- **Коллекции**: `List[T]`, `Dict[K, V]`, `Set[T]`, `Tuple[T1, T2]`. (Начиная с Python 3.9 можно использовать встроенные типы напрямую: `list[int]`, `dict[str, int]`).
- **Опциональные значения**: `Optional[T]` (эквивалентно `Union[T, None]`).

### 2. Продвинутые концепции
- **Protocol (Утиная типизация)**: позволяет задавать структурную типизацию (интерфейсы по принципу "если объект умеет это делать, значит он подходит").
- **Generic (Дженерики)**: создание обобщенных классов и функций, работающих с любыми типами данных через `TypeVar`.
- **Callable**: аннотация функций-колбэков (например, `Callable[[int, str], bool]`).

---

## Производственный пример кода

Пример использования протоколов (`Protocol`) и статической типизации в бэкенд-компонентах:

```python
from typing import Protocol, List, Optional

class Logger(Protocol):
    def log(self, message: str) -> None: ...

class ConsoleLogger:
    def log(self, message: str) -> None:
        print(f"[LOG]: {message}")

class Service:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def process(self, data: Optional[List[str]]) -> int:
        if not data:
            self.logger.log("No data provided")
            return 0
        self.logger.log(f"Processing {len(data)} items")
        return len(data)

if __name__ == "__main__":
    srv = Service(ConsoleLogger())
    count = srv.process(["item1", "item2"])
    print(f"Processed count: {count}")
    print("Type hints проверены успешно!")
```

---

## Анализ сложности (Big O)

- Статическая проверка типов выполняется **инструментом Mypy в CI/CD** перед деплоем.
- Во время выполнения программы (`runtime`) аннотации типов **не создают никаких накладных расходов** на производительность (нулевая временная сложность в продакшене).

---

## Применение в Яндексе
- **Стандарты кодирования**: Обязательный стандарт во всех современных бэкенд-сервисах на Python (FastAPI, асинхронные пайплайны).
- **Интеграция с IDE и ORM**: Автодополнение кода и ранняя проверка корректности запросов в SQLAlchemy и Pydantic.

