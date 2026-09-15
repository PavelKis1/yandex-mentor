# 📖 Лекция 27: Itertools (Работа с итераторами)

## 📝 О чем это
Модуль `itertools` предоставляет набор инструментов для создания быстрых и эффективных итераторов. Это критически важно для работы с большими объемами данных и комбинаторными задачами.

## 💡 Основные концепции
*   Бесконечные итераторы (`count`, `cycle`, `repeat`).
*   Итераторы, завершающиеся на кратчайшей входной последовательности (`chain`, `zip_longest`, `islice`).
*   Комбинаторные итераторы (`product`, `permutations`, `combinations`).

## 💻 Базовый код
```python
import itertools

# Декартово произведение
for i in itertools.product('AB', range(2)):
    print(i) # ('A', 0), ('A', 1), ('B', 0), ('B', 1)

# Группировка
for key, group in itertools.groupby([1, 1, 2, 3, 3]):
    print(key, list(group))
```

## 🚀 Сложность
Работает лениво (lazy evaluation), потребляя $O(1)$ памяти для итератора, но время генерации зависит от размера результата.

## 🔗 Ресурсы
*   [Python Docs: itertools](https://docs.python.org/3/library/itertools.html)
