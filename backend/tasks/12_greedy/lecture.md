# 📖 Лекция 12: Жадные алгоритмы (Greedy)

## Что это и зачем

Жадный алгоритм на каждом шаге выбирает локально оптимальное решение, надеясь, что это приведёт к глобальному оптимуму. Работает не всегда, но когда работает — даёт элегантное O(n log n) решение.

## Когда работает

- Задача имеет свойство **matroid** (теорема Радо-Эдмондса)
- Жадный выбор безопасен (можно доказать)
- Оптимальная подструктура

## Когда НЕ работает

- 0/1 Knapsack — не жадный (нужен DP)
- Обмен валют — иногда не жадный

## Jump Game

```python
def can_jump(nums):
    max_reach = 0
    for i, n in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + n)
    return True
```

Время: O(n), память: O(1).

## Gas Station

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            tank = 0
            start = i + 1
    return start
```

## Activity Selection

```python
def activity_selection(start, end):
    activities = sorted(zip(start, end), key=lambda x: x[1])
    count = 1
    last_end = activities[0][1]
    for s, e in activities[1:]:
        if s >= last_end:
            count += 1
            last_end = e
    return count
```

## Interval Scheduling

```python
def erase_overlap_intervals(intervals):
    if not intervals: return 0
    intervals.sort(key=lambda x: x[1])  # сортировка по концу
    count = 1
    end = intervals[0][1]
    for s, e in intervals[1:]:
        if s >= end:
            count += 1
            end = e
    return len(intervals) - count  # сколько удалить
```

## Candy (рейтинговая раздача конфет)

```python
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)
```

## Задачи на LeetCode

- Jump Game (#55)
- Jump Game II (#45)
- Gas Station (#134)
- Activity Selection / Non-overlapping Intervals (#435)
- Candy (#135)
- Partition Labels (#763)
- Task Scheduler (#621)

## Доказательство жадности

1. **Показать оптимальную подструктуру** — opt = opt_left + opt_right
2. **Жадный выбор безопасен** — есть оптимальное решение, начинающееся с жадного выбора
3. **Индукция** — после жадного выбора остаётся та же задача

## Где используется в Яндексе

- **Планировщик задач** — минимизация простоев
- **Cache replacement** — LRU, LFU
- **Routing** — Дейкстра (с приоритетной очередью)
- **Match-making** — распределение игроков

## Подводные камни

- Жадный не всегда оптимален (Knapsack)
- Нужно доказать корректность
- Off-by-one в сравнениях `>=` vs `>`