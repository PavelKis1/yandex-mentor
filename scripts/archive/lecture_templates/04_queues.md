# 📖 Лекция 04: Очереди (Queues)

## 📝 О чем это
Очередь — это структура данных типа **FIFO** (First In, First Out — "первым пришел, первым ушел"). Как очередь в магазине.

## 💡 Основные концепции
Обычный `list` плохо подходит для очередей, так как удаление первого элемента (`list.pop(0)`) имеет сложность O(n) (все элементы нужно сдвинуть).
**Используйте `collections.deque`** для реализации очередей. `deque` (double-ended queue) обеспечивает O(1) для вставки/удаления с обоих концов.

## 🛠 Популярные методы
*   `dq.append(x)`: Добавить в конец.
*   `dq.popleft()`: Удалить из начала (важный метод для очереди!).

## 💻 Базовый код
```python
from collections import deque
q = deque()
q.append(1)
q.popleft() # 1
```

## 🚀 Сложность
| Операция | Сложность |
|---|---|
| Enqueue | O(1) |
| Dequeue | O(1) |

## 🔗 Ресурсы
*   [Python Docs: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
