"""Sliding Window: максимум суммы, самая длинная подстрока, минимальное окно."""

from collections import Counter


def max_subarray_sum(nums: list[int], k: int) -> int | None:
    """O(n) — поддерживаем сумму текущего окна размера k.

    Edge cases: пустой массив, k <= 0, k > len(nums) — возвращаем None,
    отрицательные числа (окно может уменьшать сумму).
    """
    if not nums or k <= 0 or k > len(nums):
        return None
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best


def length_of_longest_substring(s: str) -> int:
    """O(n) — sliding window + множество символов в текущем окне.

    Edge cases: пустая строка, строка без повторов, все символы одинаковые.
    """
    seen: set[str] = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


def min_window(s: str, t: str) -> str:
    """O(n + m) — расширяем правый край, схлопываем левый, пока покрыли t.

    Edge cases: пустые s/t, t длиннее s, символы t отсутствуют в s — "".
    """
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    have: Counter[str] = Counter()
    required = len(need)
    formed = 0
    left = 0
    best_left = 0
    best_len = len(s) + 1
    for right, ch in enumerate(s):
        have[ch] += 1
        if ch in need and have[ch] == need[ch]:
            formed += 1
        while left <= right and formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left
            have[s[left]] -= 1
            if s[left] in need and have[s[left]] < need[s[left]]:
                formed -= 1
            left += 1
    return "" if best_len == len(s) + 1 else s[best_left:best_left + best_len]


if __name__ == "__main__":
    assert max_subarray_sum([1, 2, 3, 4], 2) == 7
    assert max_subarray_sum([], 2) is None
    assert max_subarray_sum([1], 0) is None
    assert max_subarray_sum([1, 2, 3], 5) is None
    assert max_subarray_sum([-2, -1], 1) == -1

    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("pwwkew") == 3

    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    assert min_window("", "A") == ""
    assert min_window("abc", "") == ""

    print("All tests passed")
