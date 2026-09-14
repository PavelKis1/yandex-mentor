"""Префиксные суммы: сумма подмассива, произведение без текущего, подмножество с суммой."""


def range_sum(nums: list[int], l: int, r: int) -> int:
    """O(n) подготовка + O(1) на запрос — префиксные суммы; [l, r] инклюзивно.

    Edge cases: l == r, один элемент, весь массив, l = 0.
    """
    prefix = [0] * (len(nums) + 1)
    for i, num in enumerate(nums):
        prefix[i + 1] = prefix[i] + num
    return prefix[r + 1] - prefix[l]


def product_except_self(nums: list[int]) -> list[int]:
    """O(n) — левое произведение × правое, без деления (корректно при нулях).

    Edge cases: один/два нуля, отрицательные числа, один элемент.
    """
    n = len(nums)
    result = [1] * n
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    return result


def count_subsets(nums: list[int], k: int) -> int:
    """O(n*k) — DP по сумме (рюкзак 0/1), нижняя граница по памяти.

    Edge cases: пустой массив (k=0 даёт 1), один элемент, нулевой суммовой лимит.
    """
    dp = [0] * (k + 1)
    dp[0] = 1
    for num in nums:
        if num < 0:
            raise ValueError("negative elements are not supported by knapsack DP")
        for s in range(k, num - 1, -1):
            dp[s] += dp[s - num]
    return dp[k]


if __name__ == "__main__":
    assert range_sum([1, 2, 3, 4, 5], 1, 3) == 9  # 2+3+4
    assert range_sum([5], 0, 0) == 5
    assert range_sum([1, 2, 3], 0, 2) == 6

    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, 3, -3]) == [0, 0, 9, 0, 0]
    assert product_except_self([5]) == [1]

    assert count_subsets([1, 2, 3], 3) == 2
    assert count_subsets([], 0) == 1
    assert count_subsets([1, 2, 3], 7) == 0
    assert count_subsets([0, 1], 1) == 2

    print("All tests passed")
