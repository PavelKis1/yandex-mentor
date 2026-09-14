"""Жадные алгоритмы: Jump Game, gas station, без перекрытия интервалов."""


def can_jump(nums: list[int]) -> bool:
    """O(n) — на каждом шаге обновляем максимальный достижимый индекс.

    Edge cases: пустой массив (can reach vacuously), один элемент,
    нули как ловушки в середине.
    """
    reach = 0
    for i, num in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + num)
    return True


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    """O(n) — если суммарный газ хватает, ответ существует; считаем запас.

    Edge cases: суммарный газ < суммарной стоимости (−1), один элемент,
    нулевые значения.
    """
    if sum(gas) < sum(cost):
        return -1
    total = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:
            start = i + 1
            total = 0
    return start


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    """O(n log n) — сортировка по правой границе; жадно оставляем непересекающиеся.

    Edge cases: пустой список, один интервал, все перекрываются, нет перекрытий.
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    count = 0
    prev_end = intervals[0][1]
    for start, end in intervals[1:]:
        if start < prev_end:
            count += 1
        else:
            prev_end = end
    return count


if __name__ == "__main__":
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    assert can_jump([0]) is True
    assert can_jump([2, 0, 0]) is True
    assert can_jump([]) is True

    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([5], [5]) == 0
    assert can_complete_circuit([3, 1], [1, 2]) == 0

    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([]) == 0
    assert erase_overlap_intervals([[1, 2]]) == 0

    print("All tests passed")
