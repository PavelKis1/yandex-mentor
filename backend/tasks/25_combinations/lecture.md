# 📖 Лекция 25: Комбинаторика (Combinations & Permutations)

## 📝 О чем это
Задачи на генерацию всех возможных комбинаций или перестановок элементов. Часто решаются через `itertools` или рекурсивно.

## 💡 Основные концепции
*   **Перестановки (Permutations)**: Порядок имеет значение.
*   **Сочетания (Combinations)**: Порядок не имеет значения.

## 💻 Базовый код
```python
from itertools import combinations, permutations

items = [1, 2, 3]
print(list(combinations(items, 2))) # [(1, 2), (1, 3), (2, 3)]
print(list(permutations(items, 2))) # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

## 🚀 Сложность
*   Количество перестановок n!: O(n!).
*   Количество сочетаний: C(n, k).

## 🔗 Ресурсы
*   [Python Docs: itertools](https://docs.python.org/3/library/itertools.html)
