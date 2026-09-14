# frontend — SPA платформы «Yandex Backend Mentor»

React + TypeScript + Vite + Tailwind CSS v4.

## Скрипты

| Команда | Что делает |
|---------|-----------|
| `npm run dev` | Vite dev-сервер (HMR), по умолчанию `http://localhost:5173` |
| `npm run typecheck` | Проверка типов: `tsc --noEmit` для `src/` и `vite.config.ts` |
| `npm run build` | typecheck + production-сборка в `dist/` |
| `npm run lint` | Oxlint (0 предупреждений / 0 ошибок) |
| `npm run preview` | Просмотр собранного `dist/` |

## Структура

- `src/types.ts` — типы данных API (зеркало `src/models.py` бэкенда)
- `src/api/client.ts` — тонкий fetch-клиент, base URL из `src/config.ts` (`VITE_API_URL`)
- `src/hooks/` — `useRoadmap` (роадмап + прогресс + refresh + optimistic-смена статуса) и `useTask` (данные темы)
- `src/utils/storage.ts` — безопасные обёртки над localStorage (черновики, чек-листы, позиция чтения)
- `src/components/` — презентационные компоненты:
  - `Header`, `Footer`, `ErrorBanner`, `LoadingSpinner`
  - `RoadmapView` → `ProgressSnapshot` + `StageSection` → `TaskCard`
  - `TopicModal` → `LectureView` → `LectureChapters` + `MarkdownArticle` + `Spoiler` + `ReadingProgressBar`
  - `TopicModal` → `TaskChecklist`, `ProblemCard`, `SolutionEditor`

## UX-фичи

- **Лекции**: чтение по шагам / весь текст, оглавление (чипы на мобильном, сайдбар на lg+),
  прогресс-бар, «Коротко: …» после заголовка главы, позиция и режим в localStorage.
- **Спойлеры**: разделы «Базовый код»/«Пример решения» свёрнуты до попытки решения.
- **Задания**: чек-лист (localStorage), каскадные подсказки («open hint count» в localStorage).
- **Редактор решений**: автозагрузка черновика (debounce 2с + blur, localStorage), drag&drop
  файла `.py`, кнопка «.py»; Ctrl/Cmd+Enter — отправка на менторское ревью.
- **Роадмап**: ПКМ или кнопка «···» на карточке — быстрая смена статуса `todo/wip/done`
  (optimistic + POST `/api/task/{id}/status`); виджет прогресса обучения; «Следующая тема» в модалке.

## API

Фронтенд обращается к FastAPI-бэкенду на `http://localhost:8000` (переопределяется
переменной `VITE_API_URL` через `frontend/.env`).
