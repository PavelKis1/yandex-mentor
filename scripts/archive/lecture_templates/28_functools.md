# 📖 Лекция 28: Functools (Инструменты высшего порядка)

## 📝 О чем это
Модуль `functools` предназначен для функций высшего порядка: функций, которые работают с другими функциями или возвращают их.

## 💡 Основные концепции
*   `lru_cache`: Кеширование результатов функций.
*   `partial`: Создание функций с предустановленными аргументами.
*   `wraps`: Правильное оформление декораторов.

## 💻 Базовый код
```python
from functools import lru_cache, partial

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

add_five = partial(lambda x, y: x + y, 5)
print(add_five(10)) # 15
```

## 🚀 Сложность
`lru_cache` снижает сложность вычислений с экспоненциальной до линейной для многих задач динамического программирования.

## 🔗 Ресурсы
*   [Python Docs: functools](https://docs.python.org/3/library/functools.html)
