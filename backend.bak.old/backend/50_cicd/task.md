# Задания: Cicd

## Задание 1: Пайплайн CI
Опишите шаги CI для Python-проекта: линт, тесты, сборка образа, пуша в registry.

**Пример:** `lint → test → build → push`

💡 **Подсказка:** Этапы: checkout, setup-python, pip install, pytest, docker build.

## Задание 2: Окружения
Разделите деплой dev/stage/prod через GitHub Actions: когда какой включается?

**Пример:** `dev: push в main; prod: тег v*`

💡 **Подсказка:** triggers: push/branches/tags.

## Задание 3: Кэш зависимостей
Почему кэш pip в CI экономит минуты? Как его включить в GitHub Actions?

**Пример:** `actions/cache с ключом по hash requirements.txt`

💡 **Подсказка:** cache: pip → ~/.cache/pip.
