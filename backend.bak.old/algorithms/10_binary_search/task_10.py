"""Бинарный поиск: индекс, вращённый массив, скорость поедания бананов."""


def binary_search(nums: list[int], target: int) -> int:
    """O(log n) — классический бинарный поиск на отсортированном массиве.

    Edge cases: пустой массив, один элемент, цель меньше/больше всех, дубликаты.
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def search_rotated(nums: list[int], target: int) -> int:
    """O(log n) — в каждой итерации одна из половин гарантированно отсортирована.

    Edge cases: пустой массив, массив без вращения, цель на границе вращения.
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # левая половина отсортирована
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # правая половина отсортирована
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def min_eating_speed(piles: list[int], h: int) -> int:
    """O(n log max) — бинарный поиск по скорости; если не успеть и с max — -1.

    Edge cases: пустые piles, часов меньше числа куч, одна куча, крупная куча.
    """
    if not piles:
        return 1
    low, high = 1, max(piles)

    def hours_needed(speed: int) -> int:
        return sum((p - 1) // speed + 1 for p in piles)

    while low < high:
        mid = (low + high) // 2
        if hours_needed(mid) <= h:
            high = mid
        else:
            low = mid + 1
    return low if hours_needed(low) <= h else -1


if __name__ == "__main__":
    assert binary_search([1, 2, 3, 10], 2) == 1
    assert binary_search([1, 2, 3, 10], 99) == -1
    assert binary_search([], 1) == -1
    assert binary_search([5], 5) == 0
    assert binary_search([1, 2, 2, 2, 3], 2) in (1, 2, 3)

    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([1], 1) == 0
    assert search_rotated([1, 3], 3) == 1
    assert search_rotated([], 5) == -1

    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([5], 10) == 1
    assert min_eating_speed([3, 6], 1) == -1

    print("All tests passed")
