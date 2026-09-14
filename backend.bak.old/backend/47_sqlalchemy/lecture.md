# Лекция: 47 — SQLAlchemy ORM (Работа с базами данных в Python)

## Обзор темы
SQLAlchemy — мощный инструмент для работы с реляционными базами данных в Python, сочетающий в себе мощь SQL-выражений (Core) и удобство объектно-реляционного маппинга (ORM).

---

## Подробный теоретический минимум

### 1. Архитектура SQLAlchemy
- **SQLAlchemy Core**: слой выражения SQL, работающий с таблицами, колонками и соединениями без накладных расходов ORM.
- **SQLAlchemy ORM**: маппинг таблиц баз данных на классы Python, управление жизненным циклом объектов через `Session` (Unit of Work паттерн).

### 2. Асинхронная работа (AsyncIO)
В современных асинхронных бэкенд-приложениях (например, с FastAPI) используется `AsyncSession`, позволяющая выполнять запросы к БД без блокировки event loop.

---

## Производственный пример кода

Пример описания модели и асинхронной сессии в SQLAlchemy 2.0:

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

# Создание асинхронного движка
engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
```

---

## Анализ сложности (Big O)

- Эффективность ORM зависит от правильности построения SQL-запросов и предотвращения проблемы N+1 запросов (использование `selectinload` / `joinedload`).

---

## Применение в Яндексе
- **Разработка бизнес-логики**: Управление структурой хранения данных в бэкенд-сервисах, миграции схем с помощью Alembic.

