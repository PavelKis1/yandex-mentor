# 📖 Лекция 11: Префиксные суммы (Prefix Sum)

## Что это и зачем

Префиксная сумма — массив, где `prefix[i]` = сумма элементов от 0 до i. Позволяет получить сумму любого подмассива за O(1).

## Формула

```
prefix[i] = nums[0] + nums[1] + ... + nums[i]
```

Сумма подмассива [l, r]:
```
sum(l, r) = prefix[r] - (prefix[l-1] if l > 0 else 0)
```

## Реализация

```python
def prefix_sum(nums):
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i + 1] = prefix[i] + nums[i]
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

**Время:** O(n) на построение, O(1) на запрос. **Память:** O(n).

## Product Except Self

Каждый элемент = произведение всех, кроме текущего. За O(n) без деления:

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Левая часть
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    
    # Правая часть
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    
    return result
```

## 2D Prefix Sum

```python
def prefix_sum_2d(matrix):
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = matrix[i][j] + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]
    return prefix

def rect_sum(prefix, r1, c1, r2, c2):
    return prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] - prefix[r2 + 1][c1] + prefix[r1][c1]
```

## Continuous Subarray Sum

```python
def check_subarray_sum(nums, k):
    prefix = 0
    seen = {0: -1}
    for i, num in enumerate(nums):
        prefix += num
        if k != 0:
            prefix %= k
        if prefix in seen:
            if i - seen[prefix] > 1:
                return True
        else:
            seen[prefix] = i
    return False
```

## Задачи на LeetCode

- Running Sum of 1d Array (#1480)
- Maximum Subarray (#53)
- Product Except Self (#238)
- Number of Subarrays with Sum (#930)
- Continuous Subarray Sum (#523)
- Subarray Sums Divisible by K (#974)
- Range Sum Query 2D (#304)

## Где используется в Яндексе

- **Метрики** — скользящие суммы
- **Аналитика** — DAU, revenue за период
- **Image processing** — Box filter
- **Игры** — подсчёт очков за интервал

## Подводные камни

- `prefix[i]` содержит сумму до i, не включая i — сдвиг на 1
- `-1` для prefix[0]
- 2D: не забыть вычитать twice counted region