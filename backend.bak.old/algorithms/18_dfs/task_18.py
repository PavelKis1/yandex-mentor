"""DFS: количество островов, максимальная площадь, курсы-зависимости."""


def num_islands(grid: list[list[int]]) -> int:
    """O(rows*cols) — итеративный DFS «затапливает» остров при встрече 1.

    Edge cases: пустая сетка, полностью суша/вода, остров из одной клетки.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                count += 1
                stack = [(r, c)]
                grid[r][c] = 0
                while stack:
                    x, y = stack.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                            grid[nx][ny] = 0
                            stack.append((nx, ny))
    return count


def max_area_of_island(grid: list[list[int]]) -> int:
    """O(rows*cols) — DFS-площадь каждого острова, берём максимум.

    Edge cases: пустая сетка, нет суши (0), вся сетка — один остров.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            area = 0
            stack = [(r, c)]
            grid[r][c] = 0
            while stack:
                x, y = stack.pop()
                area += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1:
                        grid[nx][ny] = 0
                        stack.append((nx, ny))
            best = max(best, area)
    return best


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """O(V + E) — поиск цикла по DFS-состояниям: 0/не посещён, 1/в обходе, 2/готов.

    Edge cases: пустой список зависимостей (True), самозависимость (False),
    курсов нет вообще (True).
    """
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    for course, dependency in prerequisites:
        graph[course].append(dependency)
    state = [0] * num_courses

    def has_cycle(node: int) -> bool:
        if state[node] == 1:
            return True
        if state[node] == 2:
            return False
        state[node] = 1
        for dependency in graph[node]:
            if has_cycle(dependency):
                return True
        state[node] = 2
        return False

    return not any(has_cycle(node) for node in range(num_courses))


if __name__ == "__main__":
    grid1 = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]
    assert num_islands(grid1) == 2
    assert num_islands([]) == 0
    assert num_islands([[0, 0], [0, 0]]) == 0
    assert num_islands([[1]]) == 1

    grid2 = [[0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 1]]
    assert max_area_of_island(grid2) == 5
    assert max_area_of_island([]) == 0
    assert max_area_of_island([[0]]) == 0
    assert max_area_of_island([[1, 1], [1, 1]]) == 4

    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(1, [[0, 0]]) is False
    assert can_finish(3, []) is True
    assert can_finish(0, []) is True

    print("All tests passed")
