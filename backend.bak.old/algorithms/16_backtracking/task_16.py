"""Backtracking: перестановки, подмножества, N-Queens."""


def permute(nums: list[int]) -> list[list[int]]:
    """O(n!) — перебор всех перестановок с флагом использованных позиций.

    Edge cases: пустой массив ([[]]), один элемент, дубликаты значений.
    """
    result: list[list[int]] = []
    n = len(nums)

    def backtrack(path: list[int], used: list[bool]) -> None:
        if len(path) == n:
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(num)
            backtrack(path, used)
            path.pop()
            used[i] = False

    backtrack([], [False] * n)
    return result


def subsets(nums: list[int]) -> list[list[int]]:
    """O(2^n) — рекурсивно: взять элемент или пропустить и двигаться дальше.

    Edge cases: пустой массив ([[]]), один элемент, все элементы одинаковые.
    """
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result


def solve_n_queens(n: int) -> list[list[str]]:
    """O(n!) — доски n×n в виде списка строк ('Q' и '.').

    Edge cases: n = 0 (пусто), n = 1 (одно решение), n = 2 и 3 (решений нет).
    """

    if n <= 0:
        return []

    def is_safe(board: list[int], row: int, col: int) -> bool:
        for r in range(row):
            if board[r] == col or abs(board[r] - col) == abs(r - row):
                return False
        return True

    solutions: list[list[str]] = []
    board = [-1] * n

    def backtrack(row: int) -> None:
        if row == n:
            solutions.append(
                [
                    "".join("Q" if col == board[r] else "." for col in range(n))
                    for r in range(n)
                ]
            )
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1

    backtrack(0)
    return solutions


if __name__ == "__main__":
    assert permute([]) == [[]]
    assert permute([1]) == [[1]]
    perms = permute([1, 2, 3])
    assert len(perms) == 6
    assert sorted(perms) == [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert sorted(permute([1, 1])) == [[1, 1], [1, 1]]

    subs = subsets([1, 2, 3])
    assert len(subs) == 8
    assert sorted(subs) == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert subsets([]) == [[]]

    assert solve_n_queens(0) == []
    assert len(solve_n_queens(1)) == 1
    assert len(solve_n_queens(4)) == 2
    assert solve_n_queens(2) == []
    assert solve_n_queens(3) == []

    print("All tests passed")
