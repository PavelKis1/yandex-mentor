# 📖 Лекция 22: Дейкстра (Dijkstra)

## Что это и зачем

Алгоритм Дейкстры — поиск кратчайшего пути от источника до всех вершин в графе с неотрицательными весами рёбер. Использует приоритетную очередь (min-heap).

## Когда использовать

- Кратчайший путь в графе с положительными весами
- Навигация (GPS)
- Сетевые маршруты
- Минимальная стоимость пути

## Шаблон

```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

## Network Delay Time

```python
def network_delay_time(times, n, k):
    graph = {i: [] for i in range(1, n + 1)}
    for u, v, w in times:
        graph[u].append((v, w))
    
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    pq = [(0, k)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    
    max_dist = max(dist.values())
    return max_dist if max_dist != float('inf') else -1
```

## Задачи на LeetCode

- Network Delay Time (#743)
- Cheapest Flights Within K Stops (#787)
- Path With Maximum Probability (#1514)
- Shortest Path to Get All Keys (#864)
- Minimum Cost to Reach Destination (#1976)

## Где используется в Яндексе

- **Навигация** — кратчайший путь
- **Маршрутизация** — сетевые пакеты
- **Планирование** — минимальная стоимость доставки
- **Графы зависимостей** — сборка проектов

## Подводные камни

- Не проверил `d > dist[u]` — устаревшая запись в очереди
- Не обработал `float('inf')` — недостижимые вершины
- Не использовал `heapq` — O(V²) вместо O(E log V)