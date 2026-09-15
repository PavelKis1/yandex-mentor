# 📖 Лекция 29: Python Internals (Внутренности Python)

## 📝 О чем это
Понимание того, как Python работает под капотом: GIL, управление памятью, модель объектов.

## 💡 Основные концепции
*   **GIL (Global Interpreter Lock)**: Позволяет исполнять только один поток Python-кода за раз.
*   **Reference Counting & Garbage Collector**: Как Python управляет памятью.
*   **Bytecode**: Во что превращается код до выполнения виртуальной машиной (PVM).

## 💻 Базовый код
```python
import sys
import dis

def example():
    return 1 + 1

# Посмотреть байткод
dis.dis(example)
# Посмотреть счетчик ссылок
print(sys.getrefcount(1))
```

## 🚀 Сложность
Влияет на понимание производительности многопоточных приложений (CPU-bound vs I/O-bound).

## 🔗 Ресурсы
*   [Python Internals](https://docs.python.org/3/c-api/index.html)
