# 📖 Лекция 08: Sliding Window

## Что это и зачем

Sliding Window — техника, при которой мы поддерживаем "окно" (подмассив/подстроку), которое скользит по данным. Это позволяет обрабатывать массивы/строки за O(n) вместо O(n²).

## Когда использовать

- Подмассив/подстрока фиксированной длины
- Подмассив/подстрока с условием (max, min, ≥, ≤)
- "Найди непрерывную последовательность..."
- "Максимум/минимум в окне размера k"

## Виды

- **Фиксированное окно** — размер k известен
- **Динамическое окно** — размер меняется (обычно 2 указателя)

## Фиксированное окно

**Max Sum Subarray of Size K:**
```python
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```
Время: O(n), память: O(1).

## Динамическое окно

**Longest Substring Without Repeating:**
```python
def length_of_longest(s):
    seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

**Minimum Window Substring:**
```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = start = end = 0
    
    for right, char in enumerate(s, 1):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        
        if missing == 0:
            while left < right and need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if not end or right - left <= end - start:
                start, end = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[start:end]
```

**Longest Substring with At Most K Distinct:**
```python
def length_k_distinct(s, k):
    count = {}
    left = 0
    for right, char in enumerate(s):
        count[char] = count.get(char, 0) + 1
        if len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
    return right - left + 1
```

## Шаблон

```python
def sliding_window(arr, k):
    left = 0
    state = ...  # инициализация
    
    for right in range(len(arr)):
        # Добавляем arr[right] в state
        ...
        
        while condition_violated(state):
            # Удаляем arr[left] из state
            ...
            left += 1
        
        # Обновляем ответ
        ans = max(ans, right - left + 1)
```

## Задачи на LeetCode

- Maximum Sum Subarray of Size K (#макс. сумма)
- Longest Substring Without Repeating Characters (#3)
- Minimum Window Substring (#76)
- Sliding Window Maximum (#239)
- Longest Repeating Character Replacement (#424)
- Permutation in String (#567)
- Minimum Size Subarray Sum (#209)

## Где используется в Яндексе

- **Rate limiter** — подсчёт запросов за последнюю минуту
- **Log analyzer** — события за последние N секунд
- **Cache eviction** — LRU
- **Streaming data** — скользящее среднее

## Подводные камни

- Не обновляешь state при сдвиге окна
- Забыл обновить left при нарушении условия
- Путаешь `right - left` vs `right - left + 1`