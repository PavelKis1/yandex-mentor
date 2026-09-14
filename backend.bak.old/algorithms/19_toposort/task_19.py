"""Топологическая сортировка: алгоритм Кана, проверка цикла, словарь инопланетян."""

from collections import deque


def topological_sort(graph: dict[int, list[int]], n: int) -> list[int]:
    """O(V + E) — алгоритм Кана: вершины с нулевой входящей степенью.

    Edge cases: граф с циклом ([]), изолированные вершины, одна вершина.
    """
    indegree = [0] * n
    for node in range(n):
        for nxt in graph.get(node, []):
            indegree[nxt] += 1
    queue = deque(node for node in range(n) if indegree[node] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []


def has_cycle(graph: dict[int, list[int]], n: int) -> bool:
    """O(V + E) — DFS-состояния 0/1/2; цикл = ребро в «текущий обход».

    Edge cases: граф без рёбер (False), самопетля (True), одна вершина.
    """
    state = [0] * n

    def dfs(node: int) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        state[node] = 2
        return False

    return any(dfs(node) for node in range(n))


def alien_order(words: list[str]) -> str:
    """O(C) — рёбра из соседних слов + топологическая сортировка букв.

    Edge cases: одно слово, пустой список, префикс-конфликт (""),
    изолированные буквы.
    """
    letters: set[str] = set("".join(words))
    graph: dict[str, set[str]] = {ch: set() for ch in letters}
    indegree = {ch: 0 for ch in letters}
    for i in range(len(words) - 1):
        first, second = words[i], words[i + 1]
        if len(first) > len(second) and first.startswith(second):
            return ""  # «abc» после «ab» — некорректный словарь
        for a, b in zip(first, second):
            if a != b:
                if b not in graph[a]:
                    graph[a].add(b)
                    indegree[b] += 1
                break
    queue = deque(ch for ch in letters if indegree[ch] == 0)
    order: list[str] = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in sorted(graph[ch]):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return "".join(order) if len(order) == len(letters) else ""


if __name__ == "__main__":
    assert topological_sort({0: [1], 1: [2], 2: []}, 3) == [0, 1, 2]
    assert topological_sort({0: [1], 1: [0], 2: []}, 3) == []
    assert topological_sort({}, 3) == [0, 1, 2]
    assert topological_sort({0: [1], 2: [1]}, 3) == [0, 2, 1]

    assert has_cycle({0: [1], 1: [0], 2: []}, 3) is True
    assert has_cycle({}, 3) is False
    assert has_cycle({0: [0]}, 1) is True
    assert has_cycle({0: [1], 1: [2]}, 3) is False

    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["a"]) == "a"
    assert alien_order([]) == ""
    assert alien_order(["abc", "ab"]) == ""

    print("All tests passed")
