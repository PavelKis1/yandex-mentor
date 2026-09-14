# 📖 Лекция 14: DP 2D (Dynamic Programming 2D)

## Что это и зачем

DP 2D — динамическое программирование с двумя измерениями. Часто используется для задач с двумя строками/массивами или для таблицы.

## Типичные задачи

- "Самая длинная общая подпоследовательность"
- "Расстояние редактирования"
- "Уникальные пути в сетке"
- "Пересекающиеся подстроки"

## Unique Paths

```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# Оптимизация памяти
def unique_paths_opt(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]
```

## Longest Common Subsequence

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

## Edit Distance

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]
```

## Triangle Minimum Path

```python
def minimum_total(triangle):
    n = len(triangle)
    dp = triangle[-1][:]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]
```

## Задачи на LeetCode

- Unique Paths (#62)
- Unique Paths II (#63)
- Longest Common Subsequence (#1143)
- Edit Distance (#72)
- Triangle (#120)
- Minimum Path Sum (#64)
- Interleaving String (#97)

## Где используется в Яндексе

- **Diff** — сравнение текстов (git diff)
- **Spell checker** — Levenshtein distance
- **Bioinformatics** — выравнивание последовательностей
- **NLP** — нечёткий поиск

## Подводные камни

- Не инициализировал первую строку/столбец
- Забыл про off-by-one (индексы)
- Не оптимизировал память (2D → 1D)
- Путаешь `max` и `min` в переходах