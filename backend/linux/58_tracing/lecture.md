# Лекция: 58 — Распределенный трейсинг (OpenTelemetry, Spans, Traces)

## Обзор темы
В микросервисной архитектуре один запрос пользователя может проходить через десятки сервисов и баз данных. Распределенный трейсинг позволяет отслеживать полный путь запроса и находить узкие места в латентности.

---

## Подробный теоретический минимум

### 1. Основные понятия
- **Trace (Трейс)**: полный путь прохождения запроса через всю систему. Состоит из древовидной структуры спанов.
- **Span (Спан)**: отдельная операция (например, HTTP-запрос, SQL-запрос к БД, вызов внешней функции). Содержит временные метки (`start_time`, `end_time`), теги (`tags`) и логи (`events`).
- **Context Propagation**: механизм передачи идентификатора трейса (`traceparent`) между сервисами через HTTP-заголовки.

---

## Производственный пример кода

Пример инициализации трейсинга с использованием OpenTelemetry в Python:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# Настройка провайдера трассировки
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("yandex.service")

if __name__ == "__main__":
    with tracer.start_as_current_span("parent_operation") as parent_span:
        parent_span.set_attribute("service.name", "gateway")
        print("Выполнение родительской операции...")
        
        with tracer.start_as_current_span("child_db_query"):
            print("Выполнение дочернего запроса к БД...")
```

---

## Применение в Яндексе
- **Отладка сложных цепочек**: Быстрое обнаружение, какой именно микросервис вызвал задержку в 3 секунды при поисковом запросе.

