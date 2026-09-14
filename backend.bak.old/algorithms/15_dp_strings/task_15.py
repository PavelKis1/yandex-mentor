"""DP на строках: палиндром, Word Break, расстояние Левенштейна."""


def longest_palindrome(s: str) -> str:
    """O(n^2) — расширение от центра (2n-1 центров × до n расширений).

    Edge cases: пустая строка, один символ, чётный палиндром, все разные символы.
    """
    def expand(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1 : right]

    best = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        if len(odd) > len(best):
            best = odd
        if len(even) > len(best):
            best = even
    return best


def word_break(s: str, word_dict: list[str]) -> bool:
    """O(n^2) — DP: dp[i] = True, если s[:i] разбивается на слова.

    Edge cases: пустая строка (True), одно длинное слово, несколько вариантов.
    """
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]


def edit_distance(s1: str, s2: str) -> int:
    """O(m*n) — DP: вставка/удаление/замена; нижняя граница памяти (2 строки).

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
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("") == ""
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("ac") in ("a", "c")

    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    assert word_break("", []) is True

    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "") == 0
    assert edit_distance("a", "") == 1

    print("All tests passed")
