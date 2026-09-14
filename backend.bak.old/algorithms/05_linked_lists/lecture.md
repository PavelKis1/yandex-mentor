# 📖 Лекция 05: Связные списки (Linked Lists)

## Что это и зачем

Связный список — коллекция узлов (nodes), где каждый узел содержит данные и указатель на следующий узел.

```
Node(1) → Node(2) → Node(3) → None
```

## Виды

- **Односвязный (Singly)** — указатель только на следующий
- **Двусвязный (Doubly)** — указатели на следующий и предыдущий
- **Кольцевой (Circular)** — последний указывает на первый

## Реализация на Python

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Создание: 1 → 2 → 3
head = ListNode(1, ListNode(2, ListNode(3)))

# Обход
while head:
    print(head.val)  # 1, 2, 3
    head = head.next
```

## Dummy Head (фиктивный узел)

Упрощает вставку/удаление в начале:
```python
dummy = ListNode(0)
dummy.next = head
# Теперь можно вставлять перед dummy без особых случаев
```

## Операции

| Операция | Время | Примечание |
|----------|-------|------------|
| доступ по индексу | O(n) | нужно пройти |
| вставка в начало | O(1) | |
| вставка в конец | O(n)* | или O(1) с tail |
| удаление | O(1)** | с указателем на предыдущий |

*с одним указателем, **с dummy head

## Два указателя

**Нахождение середины:**
```python
def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Обнаружение цикла:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Разворот:**
```python
def reverse(head):
    prev = None
    while head:
        next_node = head.next
        head.next = prev
        prev = head
        head = next_node
    return prev
```

## Задачи на LeetCode

- Reverse Linked List (#206)
- Merge Two Sorted Lists (#21)
- Linked List Cycle (#141)
- Remove Nth Node From End (#19)
- Add Two Numbers (#2)
- Palindrome Linked List (#234)

## Сравнение с массивом

| | Связный список | Массив |
|---|----------------|--------|
| доступ | O(n) | O(1) |
| вставка в начало | O(1) | O(n) |
| вставка в конец | O(n) | O(1) |
| память | указатели | компактно |

## Где используется в Яндексе

- **LRU-кэш** — связный список + хеш-таблица
- **Музыкальные плейлисты**
- **Размотка данных** — обработка потоков
- **Объединение отсортированных файлов**

## Подводные камни

- Потеря указателя на голову
- Забыл `.next` обновить
- Бесконечный цикл при развороте
- Не обработал `None` как конец