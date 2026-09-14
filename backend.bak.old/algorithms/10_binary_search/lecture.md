# 📖 Лекция 10: Бинарный поиск (Binary Search)

## Что это и зачем

Бинарный поиск — поиск элемента в отсортированном массиве за **O(log n)**. На каждом шаге делим массив пополам.

## Когда использовать

- Массив/список отсортирован
- Монотонная функция (f(x) монотонна)
- Найти границу (first true / last false)
- Поиск по ответу (answer search)

## Базовый шаблон

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**Время:** O(log n). **Память:** O(1).

## Шаблон для границ

**Первая позиция target:**
```python
def lower_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

**Последняя позиция target:**
```python
def upper_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left - 1
```

В Python: `bisect.bisect_left`, `bisect.bisect_right`.

## Поиск вращения (Rotated Sorted Array)

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # левая половина отсортирована
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # правая отсортирована
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid + 1
    return -1
```

## Поиск по ответу

**Koko Eating Bananas (минимальная скорость):**
```python
def min_speed(piles, h):
    left, right = 1, max(piles)
    while left < right:
        mid = (left + right) // 2
        hours = sum((p + mid - 1) // mid for p in piles)
        if hours <= h:
            right = mid
        else:
            left = mid + 1
    return left
```

## bisect в Python

```python
import bisect

arr = [1, 3, 4, 4, 5, 7]
bisect.bisect_left(arr, 4)   # 2 (первый индекс)
bisect.bisect_right(arr, 4)  # 4 (после последнего)
bisect.insort(arr, 6)        # вставка с сохранением порядка
```

## Задачи на LeetCode

- Binary Search (#704)
- Search in Rotated Sorted Array (#33)
- Find First and Last Position (#34)
- Search Insert Position (#35)
- Koko Eating Bananas (#875)
- Median of Two Sorted Arrays (#4)
- Find Minimum in Rotated Sorted Array (#153)

## Где используется в Яндексе

- **Поиск в логах** — bisect по времени
- **DB индексы** — B-tree поиск O(log n)
- **Параметры моделей** — гиперпараметры через бинарный поиск
- **Rate limiter** — поиск окна
- **Скоринг** — пороги классификации

## Подводные камни

- `mid = (left + right) // 2` vs `mid = left + (right - left) // 2` (переполнение)
- `<= right` vs `< right` — выбор инварианта
- Забыл вернуть `left` после цикла (для lower_bound)
- В rotated массиве — какая половина отсортирована