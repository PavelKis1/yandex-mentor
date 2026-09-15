# 📖 Лекция 16: Бэктрэкинг (Backtracking)

## 📝 О чем это
Метод полного перебора с отсечением заведомо неверных путей.

## 💡 Основные концепции
Построение решения по шагам. Если на текущем шаге решение невозможно, мы возвращаемся (backtrack) и пробуем другой вариант.

## 💻 Базовый код
```python
# Перестановки
def permute(nums):
    res = []
    def backtrack(curr, path):
        if len(path) == len(nums):
            res.append(path[:])
            return
        for n in curr:
            path.append(n)
            backtrack([x for x in curr if x != n], path)
            path.pop()
    backtrack(nums, [])
    return res
```

## 🔗 Ресурсы
*   [Wikipedia: Backtracking](https://en.wikipedia.org/wiki/Backtracking)
