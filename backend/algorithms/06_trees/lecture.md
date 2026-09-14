# 📖 Лекция 06: Деревья (Trees)

## Что это и зачем

Дерево — иерархическая структура данных с корнем и дочерними узлами. Используется для представления вложенных данных: DOM, файловая система, JSON, организационная структура.

## Бинарное дерево

Каждый узел имеет не более 2 детей: left и right.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Двоичное дерево поиска (BST)

**Инвариант:** для каждого узла все значения в левом поддереве меньше, в правом — больше.

```python
def search(root, val):
    if not root or root.val == val:
        return root
    if val < root.val:
        return search(root.left, val)
    return search(root.right, val)
```

- Вставка/поиск/удаление: **O(h)**, где h — высота
- В сбалансированном дереве: **O(log n)**
- В вырожденном: **O(n)**

## Сбалансированные деревья

- **AVL** — строго сбалансированное, разница высот поддеревьев ≤ 1
- **Red-Black** — менее строгое, но быстрее вставка/удаление
- **B-дерево** — для дисков и баз данных

## Обходы

**DFS (Depth-First):**

Pre-order (корень, лево, право):
```python
def preorder(node):
    if not node: return
    res.append(node.val)
    preorder(node.left)
    preorder(node.right)
```

In-order (лево, корень, право) — для BST даёт отсортированный:
```python
def inorder(node):
    if not node: return
    inorder(node.left)
    res.append(node.val)
    inorder(node.right)
```

Post-order (лево, право, корень):
```python
def postorder(node):
    if not node: return
    postorder(node.left)
    postorder(node.right)
    res.append(node.val)
```

**BFS — по уровням:**
```python
from collections import deque
def level_order(root):
    if not root: return []
    queue = deque([root])
    result = []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

## Heap (Куча)

- **Min-heap** — родитель ≤ детей, корень — минимум
- **Max-heap** — родитель ≥ детей, корень — максимум
- В Python: `heapq` (min-heap)

```python
import heapq
heap = [3, 1, 4, 1, 5]
heapq.heapify(heap)  # O(n)
heapq.heappush(heap, 2)  # O(log n)
min_val = heapq.heappop(heap)  # O(log n)
```

## Задачи на LeetCode

- Maximum Depth of Binary Tree (#104)
- Invert Binary Tree (#226)
- Binary Tree Level Order Traversal (#102)
- Validate BST (#98)
- Lowest Common Ancestor (#236)
- Kth Smallest in BST (#230)
- Top K Frequent Elements (#347)

## Trie (Префиксное дерево)

- Каждый узел — символ
- Путь от корня — слово
- O(m) поиск, m = длина слова

## Где используется в Яндексе

- **DOM дерево** — рендеринг страниц
- **B-деревья** в PostgreSQL
- **Trie** — автодополнение в поиске
- **AST** — компиляторы, линтеры
- **Trie в URL Shortener** — быстрый lookup

## Подводные камни

- Stack overflow на глубокой рекурсии (используй итеративный обход)
- Забыл base case
- BST не сбалансировано → O(n) вместо O(log n)