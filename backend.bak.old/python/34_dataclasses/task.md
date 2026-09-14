# Задания: Dataclasses

## Задание 1: dataclass пользователя
Опишите датакласс User с полями id: int, name: str, email: str и метод full_info()→str. Создайте экземпляр и сравните два экземпляра по равенству.

**Пример:** `User(1,'Ann','a@b') == User(1,'Ann','a@b') → True`

💡 **Подсказка:** @dataclass + frozen=True (или eq по умолчанию).

## Задание 2: Сортировка заказов
Датакласс Order(id, total: float) снабдите полями так, чтобы сортировка шла по total (убыв.), затем по id (возр.).

**Пример:** `sorted(orders) → наибольший total первым`

💡 **Подсказка:** Поле ordering=True + кастомный порядок, либо sorted(key=...).

## Задание 3: Объединение dataclass
Напишите функцию merge_users(a: User, b: User), которая возвращает нового User с полями a, но c email=b.email, если email пуст в a.

**Пример:** `merge_users(User(1,'A',''), User(2,'B','bb')) → User(1,'A','bb')`

💡 **Подсказка:** dataclasses.replace() или ручное создание.
