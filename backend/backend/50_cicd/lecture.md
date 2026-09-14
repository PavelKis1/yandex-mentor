# Лекция: 50 — CI/CD (Непрерывная интеграция и доставка)

## Обзор темы
CI/CD (Continuous Integration / Continuous Deployment) — практика автоматизации сборки, тестирования и развертывания программного обеспечения, позволяющая доставлять изменения в продакшн быстро и без ручных ошибок.

---

## Подробный теоретический минимум

### 1. Этапы CI/CD пайплайна
- **Continuous Integration (CI)**: автоматический запуск линтеров (`flake8`, `black`), статического анализа типов (`mypy`) и юнит-тестов (`pytest`) при каждом пуше в репозиторий.
- **Continuous Delivery / Deployment (CD)**: автоматическая сборка Docker-образа, пуш в реестр (Registry) и деплой на сервер или в облачный кластер.

---

## Производственный пример кода

Пример конфигурации пайплайна GitHub Actions (`.github/workflows/ci.yml`):

```yaml
name: Backend CI/CD

on:
  push:
    branches: [ "main" ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
          
      - name: Run tests
        run: pytest
```

---

## Анализ сложности (Big O)

- Автоматизация сокращает время Time-to-Market с часов ручного деплоя до минут автоматической проверки.

---

## Применение в Яндексе
- **Автоматизация релизов**: Все сервисы Яндекса проходят строгие пайплайны автоматического тестирования и бесшовного выкатывания (Rolling Update, Canary Deployments).

