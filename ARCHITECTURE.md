# ARCHITECTURE.md — Архитектура платформы «Yandex Backend Mentor»

## 1. Используемый стек и зависимости
- **Бэкенд:** Python 3.10+, FastAPI, Uvicorn, Pydantic v2, встроенные модули Python (`pathlib`, `json`, `re`, `ast`, `subprocess`, `threading`).
- **Фронтенд:** React + TypeScript (Vite), Tailwind CSS v4 + `@tailwindcss/typography`. Markdown-контент рендерится через `react-markdown` + `remark-gfm`. Логика вынесена в кастомные хуки `useRoadmap`/`useTask`, компоненты мелкозернистые (Header, RoadmapView → ProgressSnapshot → StageSection → TaskCard, TopicModal → LectureView(LectureChapters+MarkdownArticle+Spoiler+ReadingProgressBar)/TaskChecklist/ProblemCard/SolutionEditor). Проверка типов (`tsc --noEmit`) встроена в сборочный пайплайн (`npm run build` → typecheck + vite build).
- **Автоматизация и ментор:** Встроенный демон отслеживания изменений (`watchdog`), автоматический статический анализ решений (`ast` + subprocess), генерация отчетов (`data/mentor_report.md`).
- **Тесты:** pytest (`tests/`), для API — httpx/TestClient.

## 2. Структура каталогов и модули
- `server.py` — тонкая точка входа для обратной совместимости (`uvicorn server:app`); весь код — в пакете `src/`.
- `src/main.py` — сборка FastAPI-приложения (`create_app`): CORS, роутер, lifespan (подготовка `data/`/`logs/`, стартовое сканирование, запуск watcher).
- `src/config.py` — единый источник путей: `backend/` (контент), `data/` (прогресс, отчёты, состояние), `logs/` (лог-файлы).
- `src/models.py` — Pydantic-модели: `TaskSummary`, `RoadmapStage`, `TaskData`, `Problem`, `ReviewMetrics`, `Review`, `SolutionSubmit`, `StatusUpdate`, `ErrorEvent`. Поле `Problem.solution` удалено — готовые ответы не сериализуются в API.
- `src/api/routes.py` — REST-эндпоинты: `/api/roadmap`, `/api/progress`, `/api/task/{id}`, `/api/lecture/{id}`, `/api/task/{id}/review`, `/api/refresh`, `/api/report`, `/api/errors`.
- `src/core/registry.py` — реестр задач. Тема описывается файловой структурой `backend/<блок>/NN_slug/` (каталог), русские названия/навыки — в `src/core/tasks_meta.json`. Регистр является источником истины для roadmap и сканирования.
- `src/core/analyzer.py` — автопроверка решения: заглушки, `return`, type hints (через `ast`), сложность O(...), тесты, edge cases, `py_compile` + выполнение с таймаутом.
- `src/core/reports.py` — генерация `mentor_report.md`, `progress.json`, `.mentor_state.json`.
- `src/core/storage.py` — JSON-хелперы, атомарные записи (temp + `os.replace`), одноразовая миграция старых файлов из корня в `data/` и `logs/`.
- `src/core/daemon.py` — фоновый сканер (`run_mentor_scan`, single-flight через lock) и watcher на `backend/` (суффиксы `.py/.sql/.md`, игнор `__pycache__`).
- `backend/`: 69 тем учебного плана, разбитых по 7 разделам:
  - `algorithms/` (Темы 01–25: структуры данных, алгоритмы)
  - `python/` (Темы 26–35: продвинутый Python, модули, internals)
  - `databases/` (Темы 36–43: SQL, индексы, транзакции, Redis)
  - `backend/` (Темы 44–52: HTTP, REST, FastAPI, SQLAlchemy, Docker, CI/CD, Linux, Security)
  - `linux/` (Темы 53–59: процессы, сеть, файлы, логирование, метрики, трейсинг, systemd)
  - `system_design/` (Темы 60–65: архитектурные паттерны и проектирование систем)
  - `mocks/` (Темы 66–69: имитация технических собеседований)
  - Каждая тема содержит детальную лекцию (`lecture.md`) и структурированные задания (`task.md`).
- `frontend/`: клиентская часть, взаимодействующая с бэкендом через REST API.
- `data/`, `logs/`: персистентность ментора (`progress.json`, `errors.json`, `mentor_report.md`, `.mentor_state.json`) и файлы логов.
- `tests/`: unit-тесты реестра и анализатора, фикстуры в `tests/samples/`.

## 3. Модели данных и эндпоинты
- **`GET /api/roadmap`**: полная иерархическая структура учебного плана (разделы и задачи), собирается динамически из `src/core/registry.py`.
- **`GET /api/task/{task_id}`**: содержимое лекции, распарсенные задания из `task.md` и код решения пользователя. Код (`code`) возвращается только для тем со статусом `wip`/`done` — для `todo`-тем редактор стартует пустым (готовые ответы скрыты до попытки решения). В заданиях (`problems`) поля `solution` нет.
- **`POST /api/task/{task_id}/solution`**: сохраняет решение пользователя в файл темы, запускает автопроверку и обновляет статус в `progress.json`. Тело: `{"code": "..."}`. Ответ: `{status, task_id, task_status, review}`.
- **`GET /api/progress`**: статусы выполнения всех 69 тем (`todo`, `wip`, `done`).
- **`POST /api/task/{task_id}/status`**: ручная смена статуса темы (`todo`/`wip`/`done`) — используется контекстным меню карточки роадмапа (ПКМ или кнопка «···»). Отклик: `{task_id, status}`.
- **`POST /api/refresh`**: принудительный запуск сканирования и проверки решений ментором (сериализуется с watcher-сканами).

## 4. Масштабирование и точки расширения
- **Добавление новых тем**: создать каталог `backend/<блок>/NN_slug/` с `lecture.md` и `task.md`; при желании дополнить `src/core/tasks_meta.json`. Никаких правок в коде — тема автоматически появится в роадмапе и отчётах.
- **Расширение анализа**: модификация `analyze_solution` в `src/core/analyzer.py` для добавления новых проверок (лишние абстракции — не нужны, но новые AST-проверки и кастомные юнит-тесты добавляются именно там).
- **Изоляция сканирования**: `run_mentor_scan` защищён мьютексом (single-flight) и пишет файлы атомарно — watcher и ручной refresh не создают гонок.
