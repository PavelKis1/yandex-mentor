# 📖 Лекция: 42 — SQL Транзакции (Transactions)

## Обзор темы
Транзакции гарантируют целостность данных (ACID: Atomicity, Consistency, Isolation, Durability) при выполнении набора операций.

## Подробный теоретический минимум
- **ACID**: 
  - Atomicity (Атомарность): всё или ничего.
  - Consistency (Согласованность): переход из одного корректного состояния в другое.
  - Isolation (Изоляция): операции не видят незавершенных транзакций других.
  - Durability (Долговечность): результат сохраняется даже после сбоя.
- **Уровни изоляции**: Read Uncommitted, Read Committed, Repeatable Read, Serializable.

## Производственный пример кода
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- Если что-то пошло не так, используем ROLLBACK
```

## Применение в Яндексе
- Финансовые транзакции (Яндекс.Банк, оплата поездок в Такси).
