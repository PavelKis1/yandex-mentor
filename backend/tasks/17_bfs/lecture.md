# 📖 Лекция 17: BFS (Breadth-First Search)

## Что это и зачем

BFS — обход графа в ширину. Мы посещаем все узлы на текущем уровне, затем переходим на следующий. Использует очередь.

## Когда использовать

- Кратчайший путь в невзвешенном графе
- Обход дерева по уровням
- Поиск в лабиринте
- Минимальное количество шагов

## Шаблон

```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited
```

## Level Order Traversal (дерево)

```python
def level_order(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

## Shortest Path (невзвешенный граф)

```python
def shortest_path(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
```

## Rotting Oranges

```python
def oranges_rotting(grid):
    from collections import deque
    queue = deque()
    fresh = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh += 1
    
    minutes = 0
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    while queue and fresh > 0:
        for _ in range(len(queue)):
            i, j = queue.popleft()
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] == 1:
                    grid[ni][nj] = 2
                    fresh -= 1
                    queue.append((ni, nj))
        minutes += 1
    return minutes if fresh == 0 else -1
```

## Задачи на LeetCode

- Binary Tree Level Order Traversal (#102)
- Rotting Oranges (#994)
- Shortest Path in Binary Matrix (#1091)
- Word Ladder (#127)
- Perfect Squares (#279)
- Number of Islands (#200)

## Где используется в Яндексе

- **Поиск в ширину** — обход графа
- **BFS в поиске** — индексация страниц
- **Минимальный путь** — маршрутизация
- **Обход дерева** — рендеринг DOM

## Подводные камни

- Не проверил `visited` — бесконечный цикл
- Забыл `queue.popleft()` — не BFS
- Не обработал `None` в дереве
- Не обновил `fresh` в Rotting Oranges