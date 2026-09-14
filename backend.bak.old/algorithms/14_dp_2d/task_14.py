"""DP 2D: уникальные пути, LCS, расстояние редактирования."""


def unique_paths(m: int, n: int) -> int:
    """O(m*n) — one-dimensional DP, по столбцам текущего ряда.

    Edge cases: m = 0 или n = 0 (0 путей), m = 1 (1 путь), n = 1 (1 путь).
    """
    if m <= 0 or n <= 0:
        return 0
    dp = [1] * n
    for _ in range(1, m):
        for col in range(1, n):
            dp[col] += dp[col - 1]
    return dp[-1]


def longest_common_subsequence(s1: str, s2: str) -> int:
    """O(m*n) — нижняя граница памяти (2 строки), классическая LCS.

    Edge cases: одна строка пустая, обе пустые, строки без общих символов.
    """
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[n]


def edit_distance(s1: str, s2: str) -> int:
    """O(m*n) — DP: вставка, удаление, замена; нижняя граница памяти.

    Edge cases: одна строка пустая (len другой), обе пустые, идентичные строки.
    """
    m, n = len(s1), len(s2)
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[n]


if __name__ == "__main__":
    assert unique_paths(3, 7) == 28
    assert unique_paths(1, 1) == 1
    assert unique_paths(0, 5) == 0
    assert unique_paths(5, 0) == 0
    assert unique_paths(1, 10) == 1

    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "def") == 0
    assert longest_common_subsequence("", "abc") == 0
    assert longest_common_subsequence("abc", "abc") == 3

    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "") == 0
    assert edit_distance("abc", "abc") == 0
    assert edit_distance("a", "b") == 1

    print("All tests passed")
