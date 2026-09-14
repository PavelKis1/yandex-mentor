# 📖 Лекция 19: Топологическая сортировка (Topological Sort)

## Что это и зачем

Топологическая сортировка — упорядочивание вершин DAG (Directed Acyclic Graph) так, что для каждого ребра (u, v) вершина u идёт перед v.

## Когда использовать

- Сборка проектов (зависимости)
- Планирование задач
- Проверка циклов в графе
- Распределение курсов

## Kahn's Algorithm (BFS)

```python
def topological_sort(graph, n):
    in_degree = [0] * n
    for u in range(n):
        for v in graph[u]:
            in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return result if len(result) == n else []  # пустой = цикл
```

## DFS (обратный пост-ордер)

```python
def topological_sort_dfs(graph, n):
    visited = [0] * n  # 0=не, 1=в процессе, 2=завершён
    result = []
    
    def dfs(u):
        visited[u] = 1
        for v in graph[u]:
            if visited[v] == 1: return False  # цикл
            if visited[v] == 0:
                if not dfs(v): return False
        visited[u] = 2
        result.append(u)
        return True
    
    for i in range(n):
        if visited[i] == 0:
            if not dfs(i): return []
    return result[::-1]
```

## Задачи на LeetCode

- Course Schedule (#207)
- Course Schedule II (#210)
- Alien Dictionary (#269)
- Find Eventual Safe States (#802)
- Longest Increasing Path (#329)

## Где используется в Яндексе

- **CI/CD** — порядок сборки
- **Зависимости** — pip, npm
- **Планировщик** — задачи с зависимостями
- **Сборка проектов** — make, cmake

## Подводные камни

- Не проверил `len(result) == n` — значит есть цикл
- Забыл `visited[u] = 2`
- Путаешь `graph[u]` (из u в v) с обратным