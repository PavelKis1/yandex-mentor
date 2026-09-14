# 📖 Лекция 24: Строки (Strings)

## Что это и зачем

Строки — последовательности символов. В Python строки неизменяемы (immutable), поэтому операции создают новые строки.

## Основные операции

```python
s = "hello"
len(s)           # 5
s[0]             # 'h'
s[-1]            # 'o'
s[1:4]           # 'ell'
s + " world"     # конкатенация
"hello" * 3      # "hellohellohello"
"hello".upper()  # "HELLO"
"hello".lower()  # "hello"
"hello".find("l")  # 2
"hello".count("l") # 2
```

## Два указателя на строках

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

## Sliding Window на строках

```python
def longest_substring(s):
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

## KMP (Knuth-Morris-Pratt)

```python
def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1
```

## Задачи на LeetCode

- Valid Anagram (#242)
- Group Anagrams (#49)
- Longest Substring Without Repeating (#3)
- Longest Palindromic Substring (#5)
- Implement strStr (#28)
- Reverse String (#344)
- First Unique Character (#387)

## Где используется в Яндексе

- **Поиск** — индексация текстов
- **NLP** — токенизация, нормализация
- **Логирование** — парсинг строк
- **API** — валидация входных данных

## Подводные камни

- Строки неизменяемы — не делай `s[i] = 'x'`
- `find` возвращает -1, если не найдено
- `split()` без аргумента разделяет по любым пробелам
- Не проверил `len(s) == 0`