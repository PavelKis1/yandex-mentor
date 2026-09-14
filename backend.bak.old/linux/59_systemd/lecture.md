# Лекция: 59 — Управление службами в Linux (systemd и journalctl)

## Обзор темы
`systemd` — стандартная система инициализации и управления службами (daemons) в современных дистрибутивах Linux. Она отвечает за запуск сервисов при старте системы, перезапуск при сбоях и сбор логов.

---

## Подробный теоретический минимум

### 1. Unit-файлы systemd
Конфигурация служб описывается в unit-файлах (обычно в `/etc/systemd/system/`).
- **`[Service]` секция**:
  - `ExecStart`: команда для запуска приложения.
  - `Restart=always` / `on-failure`: автоматический перезапуск при падении.
  - `User`: запуск от имени определенного непривилегированного пользователя.

### 2. Управление через `systemctl` и `journalctl`
- `systemctl start / stop / restart / status service_name` — управление состоянием службы.
- `journalctl -u service_name -f` — просмотр логов конкретной службы в реальном времени.

---

## Производственный пример кода

Пример production-ready unit-файла для FastAPI приложения (`/etc/systemd/system/yandex_app.service`):

```ini
[Unit]
Description=Yandex Backend Mentor Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/yandex_review
ExecStart=/var/www/yandex_review/venv/bin/uvicorn server:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Применение в Яндексе
- **Управление демонами**: Запуск и мониторинг бэкенд-служб на виртуальных машинах и серверах без использования Docker.

