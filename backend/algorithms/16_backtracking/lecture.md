# 📖 Лекция 16: Backtracking (Поиск с возвратом)

## Что это и зачем

Backtracking — перебор с возвратом. Мы пробуем варианты, и если они не работают — возвращаемся назад. Это как ходить по лабиринту с возможностью вернуться.

## Когда использовать

- Перестановки, комбинации, подмножества
- Судоку, N-Queens
- Разбиение строки
- Поиск пути в графе с ограничениями

## Шаблон

```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])
        return
    
    for choice in choices:
        if is_valid(choice, path):
            path.append(choice)
            backtrack(path, choices)
            path.pop()  # возврат
```

## Permutations

```python
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack(path, used)
                path.pop()
                used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

## Subsets

```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

## N-Queens

```python
def solve_n_queens(n):
    result = []
    def backtrack(row, cols, diags, anti_diags, path):
        if row == n:
            result.append(path[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diags or (row + col) in anti_diags:
                continue
            cols.add(col)
            diags.add(row - col)
            anti_diags.add(row + col)
            path.append(col)
            backtrack(row + 1, cols, diags, anti_diags, path)
            path.pop()
            cols.remove(col)
            diags.remove(row - col)
            anti_diags.remove(row + col)
    backtrack(0, set(), set(), set(), [])
    return result
```

## Word Search

```python
def exist(board, word):
    def dfs(i, j, k):
        if k == len(word): return True
        if i < 0 or j < 0 or i >= len(board) or j >= len(board[0]) or board[i][j] != word[k]:
            return False
        temp = board[i][j]
        board[i][j] = '#'
        found = dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or dfs(i, j+1, k+1) or dfs(i, j-1, k+1)
        board[i][j] = temp
        return found
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if dfs(i, j, 0):
                return True
    return False
```

## Задачи на LeetCode

- Permutations (#46)
- Subsets (#78)
- N-Queens (#51)
- Word Search (#79)
- Combination Sum (#39)
- Palindrome Partitioning (#131)
- Sudoku Solver (#37)

## Где используется в Яндексе

- **Конфигурация** — подбор параметров
- **Тестирование** — генерация тест-кейсов
- **AI** — поиск в дереве решений
- **Оптимизация** — перебор вариантов

## Подводные камни

- Не сделал `path.pop()` — бесконечный рост
- Забыл `used[i] = False`
- Не проверил `is_valid` перед добавлением
- Stack overflow на глубокой рекурсии