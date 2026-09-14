"""Множества: пересечение, количество уникальных, проверка подмножества."""

from collections import Counter


def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """O(n + m) — пересечение через set, без дубликатов в ответе.

    Edge cases: пустые массивы, одинаковые массивы, дубликаты внутри массива.
    """
    return list(set(nums1) & set(nums2))


def count_unique(nums: list[int]) -> int:
    """O(n) — количество уникальных элементов через set.

    Edge cases: пустой массив, один элемент, все элементы одинаковые.
    """
    return len(set(nums))


def is_subset(small: list[int], large: list[int]) -> bool:
    """O(n + m) — мультимножественная проверка: каждый элемент small входит
    в large с нужной кратностью (дубликаты учитываются).

    Edge cases: пустой small (пустое подмножество чего угодно), пустой large,
    повторяющиеся элементы.
    """
    small_counts = Counter(small)
    large_counts = Counter(large)
    return all(small_counts[value] <= large_counts[value] for value in small_counts)


if __name__ == "__main__":
    assert intersection([1, 2, 2, 3], [2, 3, 4]) == [2, 3]
    assert intersection([], [1, 2]) == []
    assert intersection([1, 2], [1, 2]) == [1, 2]
    assert sorted(intersection([2, 2, 2], [2, 2])) == [2]

    assert count_unique([1, 2, 3]) == 3
    assert count_unique([]) == 0
    assert count_unique([7]) == 1
    assert count_unique([1, 1, 1]) == 1

    assert is_subset([1, 2], [3, 2, 1]) is True
    assert is_subset([4], [1, 2, 3]) is False
    assert is_subset([], [1, 2, 3]) is True
    assert is_subset([1, 1], [1]) is False
    assert is_subset([1, 1], [1, 1, 2]) is True

    print("All tests passed")
