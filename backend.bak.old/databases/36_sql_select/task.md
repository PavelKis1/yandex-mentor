# Задания: Sql Select

## Задание 1: Выборка с условием
Таблица users(id, name, age). Выберите имена пользователей старше 18 лет, отсортированных по возрасту по убыванию.

**Пример:** `SELECT name FROM users WHERE age > 18 ORDER BY age DESC;`

💡 **Подсказка:** WHERE + ORDER BY; экранируй кавычки.

## Задание 2: Подсчёт по группам
Таблица orders(user_id, amount). Подсчитайте для каждого пользователя суммарную сумму заказов и количество заказов.

**Пример:** `SELECT user_id, SUM(amount), COUNT(*) FROM orders GROUP BY user_id;`

💡 **Подсказка:** GROUP BY + агрегатные функции.

## Задание 3: LIMIT и OFFSET
Таблица products(price). Верните 5 самых дешёвых товаров, исключая первые 10.

**Пример:** `SELECT * FROM products ORDER BY price LIMIT 5 OFFSET 10;`

💡 **Подсказка:** ORDER BY price ASC LIMIT/OFFSET.
