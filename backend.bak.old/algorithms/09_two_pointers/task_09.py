"""Два указателя: пара чисел, удаление дубликатов, слияние отсортированных."""


def two_sum(nums: list[int], target: int) -> list[int]:
    """O(n) — nums отсортирован; сдвигаем указатели с краёв к центру.

    Возвращает два числа либо []. Edge cases: пустой/одноэлементный массив,
    отрицательные числа, отсутствие подходящей пары.
    """
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [nums[left], nums[right]]
        if total < target:
            left += 1
        else:
            right -= 1
    return []


def remove_duplicates(nums: list[int]) -> int:
    """O(n), in-place — медленный указатель хранит «хвост» уникальных.

    Edge cases: пустой массив, единственный элемент, все элементы одинаковые.
    """
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


def merge_sorted(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    """O(m + n), in-place — заполняем nums1 с конца, ничего не перезаписывая.

    Edge cases: пустой nums2 (n=0), пустой nums1 (m=0), пересекающиеся значения.
    """
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1


if __name__ == "__main__":
    assert two_sum([1, 2, 3, 4, 5], 9) == [4, 5]
    assert two_sum([], 5) == []
    assert two_sum([3], 3) == []
    assert two_sum([-5, -2, 0, 3], -2) == [-5, 3]
    assert two_sum([1, 2, 7], 5) == []

    nums = [1, 1, 2]
    assert remove_duplicates(nums) == 2
    assert nums[:2] == [1, 2]
    assert remove_duplicates([]) == 0
    assert remove_duplicates([5]) == 1
    assert remove_duplicates([2, 2, 2]) == 1

    nums1 = [1, 2, 3, 0, 0, 0]
    merge_sorted(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]
    nums1 = [0]
    merge_sorted(nums1, 0, [1], 1)
    assert nums1 == [1]
    nums1 = [4, 5, 6, 0, 0, 0]
    merge_sorted(nums1, 3, [1, 2, 3], 3)
    assert nums1 == [1, 2, 3, 4, 5, 6]
    nums1 = [1, 2, 3]
    merge_sorted(nums1, 3, [], 0)
    assert nums1 == [1, 2, 3]

    print("All tests passed")
