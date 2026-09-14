# 📖 Лекция 18: DFS (Depth-First Search)

## Что это и зачем

DFS — обход графа в глубину. Мы идём как можно глубже, затем возвращаемся назад. Использует стек (явно или через рекурсию).

## Когда использовать

- Поиск пути в лабиринте
- Обход дерева (pre/in/post-order)
- Поиск связных компонент
- Топологическая сортировка
- Обнаружение циклов

## Шаблон (рекурсия)

```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

## Шаблон (итеративный)

```python
def dfs_iterative(start):
    stack = [start]
    visited = {start}
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
```

## Number of Islands

```python
def num_islands(grid):
    def dfs(i, j):
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != '1':
            return
        grid[i][j] = '0'
        dfs(i+1, j)
        dfs(i-1, j)
        dfs(i, j+1)
        dfs(i, j-1)
    
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count
```

## Max Area of Island

```python
def max_area(grid):
    def dfs(i, j):
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]) or grid[i][j] != 1:
            return 0
        grid[i][j] = 0
        return 1 + dfs(i+1, j) + dfs(i-1, j) + dfs(i, j+1) + dfs(i, j-1)
    
    max_area = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                max_area = max(max_area, dfs(i, j))
    return max_area
```

## Course Schedule (топологическая сортировка через DFS)

```python
def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        graph[b].append(a)
    
    visited = [0] * num_courses  # 0=не посещён, 1=в процессе, 2=завершён
    
    def dfs(node):
        if visited[node] == 1: return False  # цикл
        if visited[node] == 2: return True
        visited[node] = 1
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        visited[node] = 2
        return True
    
    for i in range(num_courses):
        if visited[i] == 0:
            if not dfs(i):
                return False
    return True
```

## Задачи на LeetCode

- Number of Islands (#200)
- Max Area of Island (#695)
- Course Schedule (#207)
- Course Schedule II (#210)
- Surrounded Regions (#130)
- Clone Graph (#133)

## Где используется в Яндексе

- **Обход графа** — индексация страниц
- **Поиск циклов** — проверка зависимостей
- **Топологическая сортировка** — сборка проектов
- **DFS в деревьях** — рендеринг, парсинг

## Подводные камни

- Не проверил `visited` — бесконечный цикл
- Забыл `visited[node] = 2` после обработки
- Не обработал `None` в дереве
- Stack overflow на глубокой рекурсии