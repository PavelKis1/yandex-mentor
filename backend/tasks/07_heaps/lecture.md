# 📖 Лекция 07: Кучи (Heaps)

## Что это и зачем

Куча (heap) — полное бинарное дерево, где родитель всегда меньше (min-heap) или больше (max-heap) детей. Корень — минимум (или максимум).

## Min-Heap vs Max-Heap

- **Min-heap:** родитель ≤ детей, корень = минимум
- **Max-heap:** родитель ≥ детей, корень = максимум

## Python: heapq

`heapq` — реализация min-heap в Python.

```python
import heapq

# Создание
heap = [3, 1, 4, 1, 5, 9]
heapq.heapify(heap)  # O(n)

# Основные операции
heapq.heappush(heap, 2)      # O(log n)
min_val = heapq.heappop(heap)  # O(log n)
min_val = heap[0]              # O(1) - посмотреть без удаления

# Max-heap - храним отрицательные
max_heap = [(-x, x) for x in [3, 1, 4, 1, 5]]
heapq.heapify(max_heap)
max_val = heapq.heappop(max_heap)[1]
```

## Heap Sort

```python
def heap_sort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]
```
Время: O(n log n), память: O(n) или O(1) in-place.

## Kth Largest/Smallest

```python
# Kth largest - используем min-heap размера k
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]
```

## Top K Frequent Elements

```python
def top_k_frequent(nums, k):
    from collections import Counter
    freq = Counter(nums)
    return [x for _, x in heapq.nlargest(k, [(v, k) for k, v in freq.items()])]
```

## Merge K Sorted Lists

```python
import heapq

def mergeKLists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode(0)
    cur = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

## Priority Queue

Приоритетная очередь = heap. В Python:

```python
from queue import PriorityQueue

pq = PriorityQueue()
pq.put((2, "задача B"))
pq.put((1, "задача A"))  # высший приоритет
pq.put((3, "задача C"))
pq.get()  # ("задача A", 1)
```

## Задачи на LeetCode

- Kth Largest Element in an Array (#215)
- Top K Frequent Elements (#347)
- Find Median from Data Stream (#295)
- Merge K Sorted Lists (#23)
- Sliding Window Maximum (#239)
- IPO (#502)

## Где используется в Яндексе

- **Top K частых запросов** — мониторинг
- **Load balancing** — выбор сервера
- ** Dijkstra** — внутренняя структура
- **Scheduling** — приоритеты задач
- **Median filter** — статистика

## Подводные камни

- `heapq` — это min-heap! Для max-heap инвертируй значения
- `heapreplace` vs `heappush` + `heappop`
- Heap не гарантирует порядок между равными элементами