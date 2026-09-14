# Лекция: 56 — Структурированное логирование (Structured Logging)

## Обзор темы
Логирование — главный инструмент наблюдаемости (Observability). В современных распределенных системах текстовые логи уступают место структурированным логам в формате JSON.

---

## Подробный теоретический минимум

### 1. Уровни логирования
- **DEBUG**: детальная отладочная информация.
- **INFO**: подтверждение нормальной работы системы.
- **WARNING**: предупреждения о потенциальных проблемах (например, заканчивается место на диске).
- **ERROR**: ошибки выполнения, требующие внимания.
- **CRITICAL**: критические сбои (падение сервиса).

### 2. Структурированные логи (JSON Logging)
Вместо склеивания строк логи пишите в формате JSON (`{"level": "INFO", "msg": "User login", "user_id": 42}`). Это позволяет индексировать их в системах сбора логов (ELK Stack, ClickHouse) и быстро строить фильтры.

---

## Производственный пример кода

Пример настройки базового JSON-логирования на Python:

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": record.created
        }
        return json.dumps(log_record)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("yandex_service")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.info("Сервер успешно запущен")
```

---

## Применение в Яндексе
- **Централизованный сбор логов**: Все микросервисы отправляют JSON-логи в единое хранилище (например, ClickHouse / ELK), где дежурные инженеры настраивают алерты и трейсинг ошибок.

