# 📖 Лекция 07: Кучи (Heaps)

## 📝 О чем это
Куча (Heap) — это специализированная структура данных на основе бинарного дерева, которая поддерживает свойство кучи: родительский узел всегда больше (в Max-Heap) или меньше (в Min-Heap) своих потомков.

## 💡 Основные концепции
*   Куча идеально подходит для задач, где нужно быстро получать доступ к максимальному или минимальному элементу.
*   В Python модуль `heapq` реализует Min-Heap.

## 🛠 Популярные методы
*   `heapq.heappush(heap, item)`: Вставка элемента — O(log n).
*   `heapq.heappop(heap)`: Извлечение минимального элемента — O(log n).
*   `heapq.heapify(list)`: Преобразование списка в кучу — O(n).

## 💻 Базовый код
```python
import heapq
heap = []
heapq.heappush(heap, 10)
min_val = heapq.heappop(heap)
```

## 🚀 Сложность
*   Получение min/max: O(1).
*   Вставка/Удаление min/max: O(log n).

## 🔗 Ресурсы
*   [Python Documentation: heapq](https://docs.python.org/3/library/heapq.html)
