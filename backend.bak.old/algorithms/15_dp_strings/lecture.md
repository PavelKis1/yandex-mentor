# 📖 Лекция 15: DP на строках (DP Strings)

## Что это и зачем

DP на строках — динамическое программирование, где состояние связано с подстроками или префиксами строк.

## Longest Palindromic Substring

```python
def longest_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    
    for i in range(n):
        dp[i][i] = True
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] if length > 2 else True
                if length > max_len:
                    max_len = length
                    start = i
    return s[start:start + max_len]
```

## Word Break

```python
def word_break(s, word_dict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for word in word_dict:
            if dp[i - len(word)] and s[i - len(word):i] == word:
                dp[i] = True
                break
    return dp[len(s)]
```

## Edit Distance (Levenshtein)

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

## Longest Common Subsequence

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

## Задачи на LeetCode

- Longest Palindromic Substring (#5)
- Word Break (#139)
- Edit Distance (#72)
- Longest Common Subsequence (#1143)
- Distinct Substrings (#940)
- Palindrome Partitioning (#131)

## Где используется в Яндексе

- **Поиск** — автодополнение, исправление опечаток
- **NLP** — выравнивание текстов
- **Биология** — сравнение последовательностей ДНК
- **Проверка орфографии** — расстояние Левенштейна

## Подводные камни

- Не инициализировал `dp[i][i] = True`
- Забыл `length > 2` для палиндромов
- Путаешь `max` и `min` в переходах