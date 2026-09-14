# 📖 Лекция 20: Union-Find (Disjoint Set Union)

## Что это и зачем

Union-Find — структура для объединения множеств и проверки, принадлежат ли элементы одному множеству. Использует "родительский" массив с оптимизацией пути.

## Когда использовать

- Связные компоненты в графе
- Обнаружение циклов
- Кластеризация
- Минимальное остовное дерево (Kruskal)

## Реализация

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # сжатие пути
        return self.parent[x]
    
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
```

## Сложность

- `find`: O(α(n)) — почти O(1) (обратная функция Аккермана)
- `union`: O(α(n))

## Number of Provinces

```python
def find_circle_num(is_connected):
    n = len(is_connected)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                uf.union(i, j)
    return len({uf.find(i) for i in range(n)})
```

## Redundant Connection

```python
def find_redundant_connection(edges):
    uf = UnionFind(len(edges))
    for u, v in edges:
        if not uf.union(u - 1, v - 1):
            return [u, v]
    return []
```

## Задачи на LeetCode

- Number of Provinces (#547)
- Redundant Connection (#684)
- Accounts Merge (#721)
- Longest Consecutive Sequence (#128)
- Graph Valid Tree (#261)

## Где используется в Яндексе

- **Кластеризация** — группировка похожих объектов
- **Социальные сети** — друзья друзей
- **Сетевые топологии** — проверка связности
- **Kruskal** — минимальное остовное дерево

## Подводные камни

- Не сделал сжатие пути (`find` без рекурсии)
- Путаешь `rank` и `size`
- Не проверил `rx == ry` в `union`