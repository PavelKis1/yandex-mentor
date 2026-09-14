# Задания: Sql Groupby

## Задание 1: HAVING
Таблица sales(category, price). Найдите категории со средней ценой больше 100.

**Пример:** `SELECT category, AVG(price) FROM sales GROUP BY category HAVING AVG(price) > 100;`

💡 **Подсказка:** HAVING для фильтра агрегатов (не WHERE).

## Задание 2: Двойная группировка
Таблица events(date, platform). Подсчитайте события по дате и платформе.

**Пример:** `SELECT date, platform, COUNT(*) FROM events GROUP BY date, platform;`

💡 **Подсказка:** GROUP BY с несколькими колонками.

## Задание 3: Количество уникальных
Таблица visits(day, user_id). Сколько уникальных пользователей было каждый день?

**Пример:** `SELECT day, COUNT(DISTINCT user_id) FROM visits GROUP BY day;`

💡 **Подсказка:** COUNT(DISTINCT ...).
