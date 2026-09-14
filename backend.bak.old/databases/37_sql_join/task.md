# Задания: Sql Join

## Задание 1: INNER JOIN
Таблицы users(id, name) и orders(id, user_id, amount). Выведите имена и суммы всех заказов.

**Пример:** `SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id;`

💡 **Подсказка:** INNER JOIN через ON.

## Задание 2: LEFT JOIN + агрегация
Выведите всех пользователей и суммарную сумму их заказов, включая тех, у кого заказов нет (NULL→0).

**Пример:** `SELECT u.name, COALESCE(SUM(o.amount),0) FROM users u LEFT JOIN orders o ON u.id=o.user_id GROUP BY u.name;`

💡 **Подсказка:** LEFT JOIN + COALESCE(...,0).

## Задание 3: JOIN 3 таблиц
users, orders, items. Выведите для каждого заказа: имя пользователя и название товара.

**Пример:** `SELECT u.name, i.name FROM orders o JOIN users u ON o.user_id=u.id JOIN items i ON o.item_id=i.id;`

💡 **Подсказка:** Двойной JOIN в цепочке.
