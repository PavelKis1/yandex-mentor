# Задания: Docker Compose

## Задание 1: Compose-файл
Напишите docker-compose.yml: сервисы web (FastAPI) и db (postgres), web зависит от db.

**Пример:** `services:
  web:
    build: .
    ports: ['8000:8000']
  db:
    image: postgres:16`

💡 **Подсказка:** version, services, ports, depends_on.

## Задание 2: Переменные окружения
Прокидывайте DATABASE_URL в web-сервис через environment (не хардкодьте в коде).

**Пример:** `environment:
  - DATABASE_URL=postgres://...`

💡 **Подсказка:** 12-factor: конфиг в env.

## Задание 3: Масштабирование
Как запустить 3 реплики web-сервиса? Что нужно изменить (переменные, healthcheck)?

**Пример:** `docker compose up --scale web=3`

💡 **Подсказка:** Нужен healthcheck + общие для реплик тома.
