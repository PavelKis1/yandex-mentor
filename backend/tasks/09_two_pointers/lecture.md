# 📖 Лекция 09: Два указателя (Two Pointers)

## Что это и зачем

Техника двух указателей — два индекса двигаются по массиву/строке с разных сторон или с разной скоростью. Позволяет решить многие задачи за O(n) вместо O(n²).

## Когда использовать

- Отсортированный массив + поиск пар
- Сравнение с двух концов (палиндром, контейнер с водой)
- Слияние/разделение массивов
- Удаление дубликатов in-place
- Быстрый и медленный указатель (связные списки, циклы)

## Виды

1. **Противоположные концы** — left=0, right=n-1, сходятся к центру
2. **Одно направление** — оба идут вперёд, но с разной скоростью
3. **Head/Tail merge** — два указателя на разных массивах

## Противоположные концы

**Two Sum (отсортированный массив):**
```python
def two_sum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
```

**Container With Most Water:**
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        water = (right - left) * min(height[left], height[right])
        max_water = max(max_water, water)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water
```

**Valid Palindrome:**
```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True
```

## Одно направление (slow/fast)

**Remove Duplicates from Sorted Array:**
```python
def remove_duplicates(nums):
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

**Move Zeroes:**
```python
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
```

## Два массива

**Merge Sorted Array:**
```python
def merge(nums1, m, nums2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    while p2 >= 0:
        nums1[p] = nums2[p2]
        p2 -= 1
        p -= 1
```

## Связные списки

**Linked List Cycle:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

## Задачи на LeetCode

- Two Sum II (#167)
- Remove Duplicates from Sorted Array (#26)
- Container With Most Water (#11)
- Valid Palindrome (#125)
- 3Sum (#15)
- Trapping Rain Water (#42)
- Sort Colors (#75)

## Где используется в Яндексе

- **Merge логов** — слияние отсортированных файлов
- **Streaming** — соединение потоков
- **Текстовый поиск** — алгоритм Кнута-Морриса-Пратта
- **In-place операции** — экономия памяти

## Подводные камни

- Off-by-one: проверь `left < right` vs `left <= right`
- Не обновляешь оба указателя
- Для 3Sum — забыл пропустить дубликаты