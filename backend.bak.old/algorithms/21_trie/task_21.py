"""Trie: дерево, поиск слов на доске, замена слов на корни."""


class TrieNode:
    """Узел префиксного дерева."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False


class Trie:
    """O(L) — префиксное дерево с insert/search/startsWith.

    Edge cases: пустая строка, один символ, вставка продублированных слов.
    """

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """O(L) — вставка слова в дерево."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        """O(L) — True, если слово вставлено (не только префикс)."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        """O(L) — True, если есть слово, начинающееся с prefix."""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """O(rows*cols*4^L) — DFS по доске с отсечением по Trie.

    Edge cases: пустая доска ([[]]), нет совпадений ([]),
    слова-дубликаты (в результате — без повторов).
    """
    rows = len(board)
    cols = len(board[0]) if rows else 0
    if not rows or not cols:
        return []
    trie = Trie()
    for word in words:
        trie.insert(word)
    found: set[str] = set()

    def dfs(r: int, c: int, node: TrieNode, path: str) -> None:
        ch = board[r][c]
        if ch not in node.children:
            return
        child = node.children[ch]
        if child.is_end:
            found.add(path + ch)
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, child, path + ch)
        board[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    return list(found)


def replace_words(dictionary: list[str], sentence: str) -> str:
    """O(sum(len(root)) + len(sentence)) — замена слов на кратчайший корень.

    Edge cases: пустой словарь, пустое предложение, корень из одного
    символа, слово без корня (остаётся как есть).
    """
    trie = Trie()
    for root in dictionary:
        trie.insert(root)

    def replace(word: str) -> str:
        node = trie.root
        for i, ch in enumerate(word):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_end:
                return word[: i + 1]
        return word

    return " ".join(replace(word) for word in sentence.split())


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    assert trie.search("") is False
    trie.insert("")
    assert trie.search("") is True
    assert trie.starts_with("b") is False

    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    assert sorted(find_words(board, ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
    assert find_words([], ["a"]) == []
    assert find_words([["a"]], ["b"]) == []

    assert (
        replace_words(
            ["cat", "bat", "rat"], "the cattle was rattled by the battery"
        )
        == "the cat was rat by the bat"
    )
    assert replace_words([], "hello world") == "hello world"
    assert replace_words(["a"], "apple ant") == "a a"

    print("All tests passed")
