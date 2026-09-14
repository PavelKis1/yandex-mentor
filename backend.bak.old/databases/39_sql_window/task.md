# Задания: Sql Window

## Задание 1: ROW_NUMBER
Таблица students(class_id, score). Для каждого класса пронумеруйте студентов по убыванию балла.

**Пример:** `SELECT *, ROW_NUMBER() OVER (PARTITION BY class_id ORDER BY score DESC) rn FROM students;`

💡 **Подсказка:** Оконная функция + PARTITION BY.

## Задание 2: Скользящая сумма
Таблица sales(day, amount). Для каждого дня посчитайте накопительную сумму продаж.

**Пример:** `SELECT day, SUM(amount) OVER (ORDER BY day) FROM sales;`

💡 **Подсказка:** SUM OVER без PARTITION = по всему набору.

## Задание 3: LAG для дельты
Таблица prices(day, price). Для каждого дня добавьте разницу с предыдущим днём.

**Пример:** `SELECT day, price - LAG(price) OVER (ORDER BY day) FROM prices;`

💡 **Подсказка:** LAG(...) OVER (ORDER BY ...).
