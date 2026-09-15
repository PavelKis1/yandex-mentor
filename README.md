# Yandex Backend Mentor

Платформа для подготовки к **Yandex Backend Intern**: 69 лекций с заданиями, автопроверка решений и интерактивный роадмап.

## Что внутри

- **69 тем**: Алгоритмы (01–25) → Python (26–35) → Базы данных (36–43) → Backend (44–52) → Linux/Observability (53–59) → System Design (60–65) → Мок-собеседования (66–69)
- **Каждая тема** = `lecture.md` (теория) + `task.md` (задания) + `task_XX.py` (скелет решения)
- **FastAPI-сервер** (`src/`): API роадмапа, отдача лекций/заданий, автопроверка решений, watcher, отчёт `data/mentor_report.md`
- **React + TypeScript-фронтенд** (`frontend/`): роадмап → тема → лекция + задачи; хуки `useRoadmap`/`useTask`, Tailwind CSS, строгий typecheck при сборке

## Структура

```
yandex_review/
├── server.py                  # Тонкая точка входа (uvicorn server:app) для обратной совместимости
├── src/                       # Серверный код (пакет)
│   ├── main.py                # Сборка FastAPI-приложения, lifespan (скан + watcher)
│   ├── config.py              # Пути: backend/, data/, logs/, файлы состояния
│   ├── models.py              # Pydantic-модели (TaskData, Review, ReviewMetrics, ...)
│   ├── api/
│   │   └── routes.py          # REST-эндпоинты
│   └── core/
│       ├── registry.py        # Реестр задач: автодискавери backend/*/NN_* + tasks_meta.json
│       ├── tasks_meta.json    # Метаданные тем (русские названия, файл решения, навык)
│       ├── analyzer.py        # Автопроверка решений (AST + subprocess)
│       ├── reports.py         # Генерация mentor_report.md, progress.json
│       ├── storage.py         # JSON-хелперы, атомарные записи, миграция старых файлов
│       └── daemon.py          # Фоновый сканер + watcher (single-flight)
├── backend/                   # Контент учебного плана
│   ├── algorithms/            # 01–25: хеш-таблицы … комбинаторика
│   ├── python/                # 26–35: collections … type hints
│   ├── databases/             # 36–43: SQL, Redis
│   ├── backend/               # 44–52: HTTP … безопасность
│   ├── linux/                 # 53–59: процессы … systemd
│   ├── system_design/         # 60–65: URL shortener … scaling
│   └── mocks/                 # 66–69: мок-собеседования
│       └── NN_topic/
│           ├── lecture.md     # теория
│           ├── task.md        # задания
│           └── task_NN.py     # скелет решения (заполняется)
├── frontend/                  # React + TypeScript + Tailwind (роадмап-UI, хуки)
├── data/                      # Динамические данные:
│   ├── progress.json          #   статус задач (todo / wip / done)
│   ├── mentor_report.md       #   отчёт автопроверки (генерируется)
│   ├── .mentor_state.json     #   кэш последней проверки
│   └── errors.json            #   ошибки по задачам (пустой по умолчанию)
├── logs/                      # Файлы логов (mentor.log, server*.log)
├── scripts/                   # Вспомогательные скрипты
│   ├── deploy.py              #   публичный URL (localhost.run туннель)
│   └── generate_task_content.py  # генерация task.md для тем
├── tests/                     # pytest: test_registry.py, test_analyzer.py (+ samples/)
├── requirements.txt           # fastapi, uvicorn, watchdog
├── requirements-dev.txt       # pytest, httpx (для тестов)
├── Dockerfile                 # контейнер сервера
└── start_mentor.bat           # запуск сервера в Windows
```

## Оптимизация (Frontend)

В приложении реализовано кэширование данных на стороне клиента с использованием `localStorage`:
- **Данные роадмапа**: Загружаются моментально из кэша при старте, фоново синхронизируясь с сервером.
- **Данные тем (лекции/задания)**: Кэшируются по ID темы, минимизируя сетевые запросы при переключении между задачами.
- **Инвалидация**: Кэш автоматически обновляется при отправке решений или принудительном обновлении страницы.


## Как работает бэкенд (FastAPI)

## UX-фичи фронтенда

- **Лекции**: чтение по шагам / весь текст, оглавление (чипы на мобильном, сайдбар на lg+),
  прогресс-бар, «Коротко: …» после заголовка главы, позиция и режим в localStorage.
- **Спойлеры**: разделы «Базовый код»/«Пример решения» свёрнуты до попытки решения.
- **Задания**: чек-лист (localStorage), каскадные подсказки («open hint count» в localStorage).
- **Редактор решений**: автозагрузка черновика (debounce 2с + blur, localStorage), drag&drop
  файла `.py`, кнопка «.py»; Ctrl/Cmd+Enter — отправка на менторское ревью.
- **Роадмап**: ПКМ или кнопка «···» на карточке — быстрая смена статуса `todo/wip/done`
  (optimistic + POST `/api/task/{id}/status`); виджет прогресса обучения; «Следующая тема» в модалке.


Бэкенд реализован на **FastAPI** и выполняет роль API-сервера, менеджера задач и системы автопроверки решений.

### Поток запроса
1.  **Аутентификация**: Каждый запрос проходит через `authenticate` (HTTP Basic Auth), проверяющий `AUTH_USER` и `AUTH_PASS` из переменных окружения.
2.  **Маршрутизация**: Запрос попадает в `src/api/routes.py`, который делегирует работу бизнес-логике.
3.  **Бизнес-логика**:
    *   Роадмап и прогресс: Чтение/запись JSON-файлов в `data/`.
    *   Задачи и лекции: `registry.py` динамически сканирует `backend/tasks/` и строит структуру тем.
    *   Проверка решений: `checker.py` выполняет код пользователя в изолированной среде, проверяя его на соответствие тестам (assert).

### Компоненты системы
*   `src/core/registry.py`: Реестр тем и задач (автодискавери).
*   `src/core/analyzer.py`: Анализ кода пользователя (AST, синтаксис, выполнение).
*   `src/core/storage.py`: Утилиты для работы с файловой системой (JSON-хранилища).
*   `src/main.py`: Сборка приложения, Middleware (CORS, логирование), аутентификация.

### Хранение данных (`data/`)
*   `progress.json`: Состояние каждой темы (`todo`/`wip`/`done`).
*   `errors.json`: База ошибок пользователей для подсказок.


## Как работает бэкенд (FastAPI)

Бэкенд реализован на **FastAPI** и выполняет роль API-сервера, менеджера задач и системы автопроверки решений.

### Поток запроса
1.  **Аутентификация**: Каждый запрос проходит через `authenticate` (HTTP Basic Auth), проверяющий `AUTH_USER` и `AUTH_PASS` из переменных окружения.
2.  **Маршрутизация**: Запрос попадает в `src/api/routes.py`, который делегирует работу бизнес-логике.
3.  **Бизнес-логика**:
    *   Роадмап и прогресс: Чтение/запись JSON-файлов в `data/`.
    *   Задачи и лекции: `registry.py` динамически сканирует `backend/tasks/` и строит структуру тем.
    *   Проверка решений: `checker.py` выполняет код пользователя в изолированной среде, проверяя его на соответствие тестам (assert).

### Компоненты системы
*   `src/core/registry.py`: Реестр тем и задач (автодискавери).
*   `src/core/analyzer.py`: Анализ кода пользователя (AST, синтаксис, выполнение).
*   `src/core/storage.py`: Утилиты для работы с файловой системой (JSON-хранилища).
*   `src/main.py`: Сборка приложения, Middleware (CORS, логирование), аутентификация.

### Хранение данных (`data/`)
*   `progress.json`: Состояние каждой темы (`todo`/`wip`/`done`).
*   `errors.json`: База ошибок пользователей для подсказок.



## Как запустить

```bash
# 1) Сервер (API + автопроверка): http://localhost:8000
pip install -r requirements.txt
py -m uvicorn server:app --host 0.0.0.0 --port 8000
# или на Windows: start_mentor.bat

# 2) Фронтенд (отдельный терминал): http://localhost:5173
cd frontend
npm install
npm run dev
```

Второй вариант: один контейнер

```bash
docker build -t yandex-mentor .
docker run -p 8000:8000 yandex-mentor
```

## Тесты

```bash
pip install -r requirements-dev.txt
py -m pytest tests -v
```

Покрывают основное: автодискавери 69 тем, форму роадмапа, анализ решений (заглушки,
type hints, синтаксис, падающие тесты, отсутствующие файлы).

## Публичный доступ (телефон/планшет)

```bash
py scripts/deploy.py   # туннель localhost.run → выдаёт URL вида https://xxx.lhr.life
# Фронтенд при этом должен быть доступен на http://localhost:5173
```

## 7 блоков роадмапа

| # | Блок | Темы | Статус |
|---|------|------|--------|
| 1 | Algorithms | 01–25 | текущий |
| 2 | Python | 26–35 | следующий |
| 3 | Databases | 36–43 | — |
| 4 | Backend | 44–52 | — |
| 5 | Linux & Observability | 53–59 | — |
| 6 | System Design | 60–65 | — |
| 7 | Mocks | 66–69 | — |

## API

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/roadmap` | Структура роадмапа (блоки + темы) |
| GET | `/api/progress` | Статус всех 69 задач |
| GET | `/api/task/{id}` | Лекция + задание + код решения темы |
| GET | `/api/lecture/{id}` | Лекция + задание темы |
| GET | `/api/task/{id}/review` | Детальная автопроверка решения |
| POST | `/api/refresh` | Перезапустить полную проверку |
| GET | `/api/report` | Текущий `mentor_report.md` |
| POST | `/api/errors` | Записать ошибку по задаче |
| GET | `/api/errors` | Все ошибки |

Документация Swagger: `http://localhost:8000/docs`

## Автопроверка решений

При старте сервер сканирует все `task_*.py` (анализ — `src/core/analyzer.py`):
детект заглушек (`...`/`pass`), наличие `return`, type hints через `ast`, комментарий
сложности O(...), тесты (`assert` в `__main__`), edge cases, синтаксис и выполнение
файла. Результат — в `data/progress.json` и `data/mentor_report.md`.
Watcher перепроверяет при изменении файла в `backend/`. Параллельные сканирования
(watcher и POST `/api/refresh`) сериализуются.

Требования к каждому решению:

- Type hints на всех функциях
- Комментарий Big O
- Тесты в `if __name__ == "__main__":` с `assert`
- Edge cases: empty, single, negative, duplicate, null

## Реестр задач и добавление новой темы

Структура тем не захардкожена: `src/core/registry.py` сканирует `backend/*/NN_*`.
Русские названия и навыки берутся из `src/core/tasks_meta.json`.

Чтобы добавить тему:
1. Создайте каталог `backend/<блок>/NN_slug/` с `lecture.md` и `task.md`;
2. При желании добавьте запись в `src/core/tasks_meta.json` (иначе название
   подставится из первой строки `task.md` вида `# Задания: <Название>`);
3. Перезапустите сервер (или вызовите `POST /api/refresh`) — тема появится в роадмапе.