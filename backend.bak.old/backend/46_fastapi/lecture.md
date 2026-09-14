# Лекция: 46 — FastAPI и Pydantic (Современный Python Backend)

## Обзор темы
FastAPI — современный, быстрый (высокопроизводительный) веб-фреймворк для создания RESTful API на Python 3.8+, основанный на стандартных аннотациях типов Python и библиотеке Pydantic.

---

## Подробный теоретический минимум

### 1. Ключевые особенности FastAPI
- **Асинхронность (ASGI)**: нативная поддержка `async/await` благодаря ASGI-серверам (Uvicorn, Hypercorn).
- **Автоматическая документация**: интерактивная документация Swagger UI (`/docs`) и ReDoc (`/redoc`), генерируемая автоматически на основе OpenAPI.
- **Интеграция с Pydantic**: декларативная валидация входящих данных и сериализация ответов с помощью моделей Pydantic.
- **Внедрение зависимостей (Dependency Injection)**: мощная встроенная система управления зависимостями через `Depends()`.

---

## Производственный пример кода

Пример создания CRUD-эндпоинтов с валидацией Pydantic:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Yandex Service API")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: int = Field(..., ge=18)

@app.post("/users/", status_code=201)
def create_user(user: UserCreate):
    return {"message": f"User {user.username} created successfully", "data": user.dict()}
```

---

## Анализ сложности (Big O)

- Производительность FastAPI сопоставима с NodeJS и Go благодаря легковесному ASGI-ядру Starlette.

---

## Применение в Яндексе
- **Микросервисная архитектура**: Основной фреймворк для разработки современных бэкенд-сервисов, внутренних API и асинхронных шлюзов.

