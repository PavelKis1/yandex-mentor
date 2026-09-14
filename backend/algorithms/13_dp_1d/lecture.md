# 📖 Лекция 13: DP 1D (Dynamic Programming 1D)

## Что это и зачем

DP 1D — динамическое программирование с одним измерением. Мы храним массив `dp[i]`, где `i` — состояние задачи.

## Когда использовать

- "Найди максимальную/минимальную сумму подмассива"
- "Можно ли достичь цели с данными шагами"
- "Минимальное количество операций"
- "Максимальная сумма без соседних элементов"

## Формула

```
dp[i] = оптимальное решение для подзадачи размера i
```

Переход:
```
dp[i] = max/min(dp[i-1], dp[i-2] + ..., dp[i-k] + ...)
```

## Climbing Stairs

```python
def climb_stairs(n):
    if n <= 2: return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

Оптимизация памяти: храним только 2 последних значения.

## House Robber

```python
def rob(nums):
    if not nums: return 0
    if len(nums) == 1: return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    return dp[-1]
```

## Coin Change

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

## Maximum Subarray (Kadane)

```python
def max_subarray(nums):
    max_ending = max_so_far = nums[0]
    for num in nums[1:]:
        max_ending = max(num, max_ending + num)
        max_so_far = max(max_so_far, max_ending)
    return max_so_far
```

## Задачи на LeetCode

- Climbing Stairs (#70)
- House Robber (#198)
- Coin Change (#322)
- Maximum Subarray (#53)
- Maximum Product Subarray (#152)
- Word Break (#139)
- Decode Ways (#91)

## Где используется в Яндексе

- **Оптимизация маршрутов** — минимальная стоимость пути
- **Планирование ресурсов** — распределение задач
- **Анализ данных** — максимальная сумма за период
- **Игры** — подсчёт очков

## Подводные камни

- Не инициализировал `dp[0]`
- Забыл обработать базовые случаи
- Перепутал `max` и `min`
- Не оптимизировал память (O(n) → O(1))