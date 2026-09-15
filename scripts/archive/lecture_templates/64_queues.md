# 📖 Лекция 64: Queues (Очереди сообщений)

## 📝 О чем это
Асинхронная обработка задач.

## 💡 Основные концепции
*   **Брокеры**: RabbitMQ, Kafka.
*   **Паттерны**: Producer-Consumer, Task Queue.

## 💻 Базовый код
```python
# Celery task
@app.task
def send_email(email):
    # отправка
    pass
```

## 🚀 Сложность
$O(1)$ для постановки в очередь.

## 🔗 Ресурсы
*   [Celery Documentation](https://docs.celeryproject.org/)
