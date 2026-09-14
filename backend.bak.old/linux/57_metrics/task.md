# Задания: Metrics

## Задание 1: Prometheus
Какие метрики вы бы собирали для HTTP API: счётчики, гистограммы?

**Пример:** `http_requests_total, http_request_duration_seconds`

💡 **Подсказка:** Counter + Histogram.

## Задание 2: RED-метрики
Назовите три метрики для сервиса: Rate, Errors, Duration. Как их измерить?

**Пример:** `RPS, error rate, latency (p99)`

💡 **Подсказка:** RED = Rate/Errors/Duration.

## Задание 3: Алерты
Сформулируйте алерт: '95% запросов медленнее 1 с в течение 5 минут' в PromQL.

**Пример:** `histogram_quantile(0.95, rate(...[5m])) > 1`

💡 **Подсказка:** PromQL + alerting rules.
