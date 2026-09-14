"""Комбинаторика: сочетания C(n,k), перестановки, подмножества."""


def combine(n: int, k: int) -> list[list[int]]:
    """O(C(n,k)) — все k-элементные подмножества [1..n].

    Edge cases: k = 0 ([[]]), k = n (одна комбинация), k > n ([]).
    """
    result: list[list[int]] = []

    def backtrack(start: int, path: list[int]) -> None:
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result


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
    """O(2^n) — рекурсивно: добавить элемент или перейти дальше.

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


if __name__ == "__main__":
    assert combine(4, 2) == [
        [1, 2],
        [1, 3],
        [1, 4],
        [2, 3],
        [2, 4],
        [3, 4],
    ]
    assert combine(3, 3) == [[1, 2, 3]]
    assert combine(3, 0) == [[]]
    assert combine(3, 4) == []

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

    print("All tests passed")
