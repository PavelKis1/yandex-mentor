"""BFS: обход по уровням, гниющие апельсины, кратчайший путь в графе."""

from collections import deque


class TreeNode:
    """Узел бинарного дерева."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def level_order(root: TreeNode | None) -> list[list[int]]:
    """O(n) — BFS с разбиением по текущей длине очереди (уровень за уровень).

    Edge cases: пустое дерево, один узел, вырожденное дерево (цепочка).
    """
    if root is None:
        return []
    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        level: list[int] = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result


def oranges_rotting(grid: list[list[int]]) -> int:
    """O(rows*cols) — мультиисточниковый BFS от «гнилых» апельсинов.

    Edge cases: пустая сетка, нет свежих (0 минут), недостижимые свежие (-1).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if not rows or not cols:
        return 0
    fresh = 0
    queue: deque[tuple[int, int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue:
        r, c, t = queue.popleft()
        minutes = max(minutes, t)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, t + 1))
    return -1 if fresh else minutes


def shortest_path(graph: dict[int, list[int]], start: int, end: int) -> int:
    """O(V + E) — BFS в невзвешенном графе (смежность: node -> neighbours).

    Edge cases: start == end (0), изолированная вершина, недостижимый конец (-1).
    """
    if start == end:
        return 0
    queue: deque[tuple[int, int]] = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1


if __name__ == "__main__":
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert level_order(root) == [[3], [9, 20], [15, 7]]
    assert level_order(None) == []
    assert level_order(TreeNode(1)) == [[1]]

    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0
    assert oranges_rotting([]) == 0

    assert shortest_path({0: [1, 2], 1: [2], 2: [3], 3: []}, 0, 3) == 2
    assert shortest_path({0: [1], 1: [0]}, 0, 0) == 0
    assert shortest_path({0: [1]}, 0, 5) == -1
    assert shortest_path({}, 1, 2) == -1

    print("All tests passed")
