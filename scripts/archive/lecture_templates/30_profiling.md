# 📖 Лекция 30: Profiling (Профилирование)

## 📝 О чем это
Как найти узкие места в производительности вашего Python-кода.

## 💡 Основные концепции
*   **Time profiling**: Сколько времени занимает выполнение кода (`timeit`, `cProfile`).
*   **Memory profiling**: Сколько памяти потребляет код (`memory_profiler`).

## 💻 Базовый код
```python
import cProfile

def my_func():
    return sum(range(1000))

cProfile.run('my_func()')
```

## 🚀 Сложность
$O(N)$ для анализа — профилирование замедляет выполнение кода, но дает точную картину.

## 🔗 Ресурсы
*   [Python Profiling](https://docs.python.org/3/library/profile.html)
