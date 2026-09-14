"""Деревья: DFS-обход, максимальная глубина, проверка BST."""


class TreeNode:
    """Узел бинарного дерева."""

    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def dfs(root: TreeNode | None) -> list[int]:
    """O(n) — итеративный обход в глубину (preorder: корень, левый, правый).

    Edge cases: пустое дерево, один узел, вырожденное дерево (цепочка).
    """
    if root is None:
        return []
    result: list[int] = []
    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


def max_depth(root: TreeNode | None) -> int:
    """O(n) — рекурсивно: глубина пустого дерева = 0.

    Edge cases: пустое дерево, один узел, несимметричное дерево.
    """
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_valid_bst(root: TreeNode | None) -> bool:
    """O(n) — каждый узел проверяется на диапазон (low, high).

    Edge cases: пустое дерево (валидно), один узел, дубликат значения,
    нарушение в правом поддереве левого узла.
    """

    def validate(node: TreeNode | None, low: int, high: int) -> bool:
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(
            node.right, node.val, high
        )

    return validate(root, -(2**63), 2**63)


if __name__ == "__main__":
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    root = TreeNode(
        1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, None, TreeNode(6)),
    )
    assert dfs(root) == [1, 2, 4, 5, 3, 6]
    assert dfs(None) == []
    assert dfs(TreeNode(7)) == [7]

    assert max_depth(root) == 3
    assert max_depth(None) == 0
    assert max_depth(TreeNode(1)) == 1
    assert max_depth(TreeNode(1, TreeNode(2))) == 2

    assert is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3))) is True
    assert is_valid_bst(None) is True
    assert is_valid_bst(TreeNode(2, TreeNode(2), TreeNode(3))) is False
    bad = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(bad) is False

    print("All tests passed")
