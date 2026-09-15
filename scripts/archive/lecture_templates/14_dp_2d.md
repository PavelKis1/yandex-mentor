# 📖 Лекция 14: Динамическое программирование 2D (DP 2D)

## 📝 О чем это
Расширение ДП на двумерные структуры. Часто применяется в задачах на сетках, матрицах или сравнении строк.

## 💡 Основные концепции
Состояние `dp[i][j]` зависит от значений в предыдущих строках или столбцах.

## 💻 Базовый код
```python
# Уникальные пути в сетке
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
```

## 🔗 Ресурсы
*   [GeeksforGeeks: 2D DP](https://www.geeksforgeeks.org/dynamic-programming-2d/)
