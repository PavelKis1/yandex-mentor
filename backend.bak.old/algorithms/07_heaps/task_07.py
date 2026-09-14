"""Кучи: k-й наибольший, слияние k списков, топ-k частых."""

import heapq
from collections import Counter


def find_kth_largest(nums: list[int], k: int) -> int:
    """O(n log k) — min-heap фиксированного размера k хранит k наибольших.

    Edge cases: k = 1, k = len(nums), отрицательные числа, дубликаты.
    """
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


def merge_k_lists(lists: list[list[int]]) -> list[int]:
    """O(n log k) — куча из (значение, индекс списка, позиция внутри списка).

    Edge cases: пустой вход, пустые списки-«заглушки», списки разной длины.
    """
    heap: list[tuple[int, int, int]] = []
    for i, lst in enumerate(lists):
        if lst:
            heap.append((lst[0], i, 0))
    heapq.heapify(heap)
    result: list[int] = []
    while heap:
        value, i, j = heapq.heappop(heap)
        result.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """O(n log k) — Counter и nlargest по частоте.

    Edge cases: один уникальный элемент, все элементы одинаковые, k = n.
    """
    counts = Counter(nums)
    return [
        value for value, _ in heapq.nlargest(k, counts.items(), key=lambda item: item[1])
    ]


if __name__ == "__main__":
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([-1, -5, -3], 1) == -1
    assert find_kth_largest([7], 1) == 7

    assert merge_k_lists([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_lists([]) == []
    assert merge_k_lists([[], []]) == []
    assert merge_k_lists([[1], [], [2, 3]]) == [1, 2, 3]

    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent([1, 2, 3], 3)) == [1, 2, 3]

    print("All tests passed")
