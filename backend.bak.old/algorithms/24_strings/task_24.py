"""Строки: анаграмма, группировка анаграмм, подстрока без повторов."""


def is_anagram(s: str, t: str) -> bool:
    """O(n) — подсчёт символов через фиксированный массив 26 букв (a-z).

    Edge cases: разная длина (False), пустые строки (True).
    """
    if len(s) != len(t):
        return False
    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - 97] += 1
    for ch in t:
        freq[ord(ch) - 97] -= 1
    return all(f == 0 for f in freq)


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """O(n * k log k) — ключ: отсортированная строка, одна итерация по strs.

    Edge cases: пустой список, один элемент, все анаграммы, ни одной пары.
    """
    groups: dict[str, list[str]] = {}
    for s in strs:
        key = "".join(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())


def length_of_longest_substring(s: str) -> int:
    """O(n) — скользящее окно: набор уникальных символов, расширяем/сжимаем.

    Edge cases: пустая строка (0), один символ (1), все символы уникальны.
    """
    seen: set[str] = set()
    lo = 0
    best = 0
    for hi, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[lo])
            lo += 1
        seen.add(ch)
        best = max(best, hi - lo + 1)
    return best


if __name__ == "__main__":
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("", "") is True
    assert is_anagram("a", "ab") is False

    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert {frozenset(g) for g in result} == {
        frozenset(["eat", "tea", "ate"]),
        frozenset(["tan", "nat"]),
        frozenset(["bat"]),
    }
    assert group_anagrams([]) == []
    assert group_anagrams(["a"]) == [["a"]]

    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("abcdef") == 6

    print("All tests passed")
