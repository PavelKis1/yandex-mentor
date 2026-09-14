# Задания: Systemd

## Задание 1: Unit-файл
Напишите service-юнит для uvicorn-приложения с рестартом при падении (Restart=always).

**Пример:** `[Service]
ExecStart=...
Restart=always
[Install]
WantedBy=multi-user.target`

💡 **Подсказка:** Управление: systemctl enable/start.

## Задание 2: Логи
Как посмотреть логи сервиса myapp без выхода в файл?

**Пример:** `journalctl -u myapp -f`

💡 **Подсказка:** journalctl -u, -f follow.

## Задание 3: Автозапуск
Чтобы сервис запускался при загрузке ОС, нужно...

**Пример:** `systemctl enable myapp`

💡 **Подсказка:** enable создаёт симлинк в multi-user.target.
