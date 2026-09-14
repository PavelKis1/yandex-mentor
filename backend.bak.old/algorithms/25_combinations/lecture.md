# 📖 Лекция 25: Комбинаторика (Combinations)

## Что это и зачем

Комбинаторика — подсчёт комбинаций, перестановок, подмножеств. Часто решается через backtracking или математические формулы.

## Формулы

- **Перестановки:** P(n, k) = n! / (n-k)!
- **Комбинации:** C(n, k) = n! / (k! * (n-k)!)
- **Подмножества:** 2^n

## Python: itertools

```python
from itertools import permutations, combinations, product

# Перестановки
list(permutations([1, 2, 3]))  # 6 штук

# Комбинации
list(combinations([1, 2, 3, 4], 2))  # 6 штук

# Декартово произведение
list(product([1, 2], ['a', 'b']))  # 4 пары
```

## Backtracking для комбинаций

```python
def combine(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    backtrack(1, [])
    return result
```

## Subsets (все подмножества)

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

## Letter Combinations of Phone Number

```python
def letter_combinations(digits):
    if not digits: return []
    mapping = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
               "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    result = []
    def backtrack(index, path):
        if index == len(digits):
            result.append("".join(path))
            return
        for char in mapping[digits[index]]:
            path.append(char)
            backtrack(index + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

## Задачи на LeetCode

- Combinations (#77)
- Permutations (#46)
- Subsets (#78)
- Letter Combinations (#17)
- N-Queens (#51)
- Combination Sum (#39)

## Где используется в Яндексе

- **A/B тесты** — комбинации вариантов
- **Конфигурация** — подбор параметров
- **Тестирование** — генерация тест-кейсов
- **AI** — поиск в дереве решений

## Подводные камни

- Не сделал `path.pop()` — бесконечный рост
- Забыл `start` в backtrack — дубликаты
- Путаешь `permutations` и `combinations`