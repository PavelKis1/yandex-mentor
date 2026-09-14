# 📖 Лекция 04: Очереди (Queue)

## Что это и зачем

Очередь — структура данных FIFO (First In, First Out). Элемент, который добавлен первым, удаляется первым. Это как очередь в магазине.

## Как работает

- `enqueue(x)` — добавить в конец
- `dequeue()` — удалить из начала
- `peek()` — посмотреть первый без удаления
- `is_empty()` — проверить пустоту

## Реализации в Python

**collections.deque — лучший вариант:**
```python
from collections import deque
q = deque()
q.append(1)      # enqueue
q.append(2)
x = q.popleft()  # dequeue → 1
x = q[0]         # peek
```

**queue.Queue — потокобезопасная:**
```python
from queue import Queue
q = Queue()
q.put(1)
x = q.get()
```

## Сложность

| Операция | Сложность |
|----------|-----------|
| enqueue | O(1) |
| dequeue | O(1) с deque |
| peek | O(1) |
| поиск | O(n) |

❗ `list.pop(0)` — O(n), не используй для очереди.

## Виды очередей

- **Обычная** — FIFO
- **Двусторонняя (deque)** — добавление/удаление с обоих концов
- **Приоритетная (heapq)** — первый элемент с минимальным приоритетом
- **Циклическая** — фиксированный размер, переиспользует память

## Задачи на LeetCode

- Implement Queue using Stacks (#232)
- Number of Recent Calls (#933)
- Sliding Window Maximum (#239)
- Design Circular Queue (#622)
- Time Needed to Buy Tickets (#2073)

## Где используется в Яндексе

- **BFS** в графах (обход в ширину)
- **Очереди задач** в Celery/RQ
- **Kafka/RabbitMQ** — обработка сообщений
- **Rate limiting** — подсчёт запросов за окно

## Подводные камни

- `list.pop(0)` — O(n), используй `deque.popleft()`
- Приоритетная очередь в Python — `heapq` (min-heap)
- Для потокобезопасности — `queue.Queue`

## Мнемоника

> **FIFO** = **F**irst **I**n, **F**irst **O**ut
> "Кто первый встал, того и тапки" — но для данных.