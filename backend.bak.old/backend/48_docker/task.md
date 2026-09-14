# Задания: Docker

## Задание 1: Dockerfile
Напишите Dockerfile для Python-приложения: установка зависимостей, копирование кода, запуск uvicorn.

**Пример:** `FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn", "server:app"]`

💡 **Подсказка:** Слои: базовый → зависимости → код.

## Задание 2: Команды
Объясните разницу между COPY и ADD, RUN и CMD.

**Пример:** `COPY копирует, ADD распаковывает архивы; RUN — build-time, CMD — runtime`

💡 **Подсказка:** Минимальный образ: python:3.11-slim.

## Задание 3: Уменьшение образа
Образ весит 1.5 ГБ. Какие действия уменьшат его до ~200 МБ?

**Пример:** `multi-stage build, python:*-slim, --no-cache-dir`

💡 **Подсказка:** multi-stage + slim + dockerignore.
