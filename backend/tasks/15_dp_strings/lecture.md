# 📖 Лекция 15: ДП на строках (DP on Strings)

## 📝 О чем это
Класс задач ДП, работающих со строками (расстояние редактирования, LCS и др.).

## 💡 Основные концепции
Состояние обычно `dp[i][j]` — результат для префикса первой строки длины `i` и второй длины `j`.

## 💻 Базовый код
```python
# Наибольшая общая подпоследовательность
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

## 🔗 Ресурсы
*   [Wikipedia: Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence)
