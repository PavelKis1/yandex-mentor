"""Связные списки: разворот, середина списка, обнаружение цикла."""


class ListNode:
    """Узел односвязного списка."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next


def reverse_list(head: ListNode | None) -> ListNode | None:
    """O(n) — перевешиваем next на предыдущий, O(1) памяти.

    Edge cases: пустой список, один узел.
    """
    prev: ListNode | None = None
    current = head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev


def middle_node(head: ListNode | None) -> ListNode | None:
    """O(n) — два указателя: fast движется вдвое быстрее slow.

    Edge cases: пустой список, один узел, чётное и нечётное число узлов.
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
    return slow


def has_cycle(head: ListNode | None) -> bool:
    """O(n) — алгоритм Флойда «черепаха и заяц».

    Edge cases: пустой список, цикл из одного узла, цикл в конце списка.
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next  # type: ignore[union-attr]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def _build(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def _to_list(head: ListNode | None) -> list[int]:
    result: list[int] = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    assert _to_list(reverse_list(_build([1, 2, 3]))) == [3, 2, 1]
    assert _to_list(reverse_list(_build([]))) == []
    assert _to_list(reverse_list(_build([5]))) == [5]

    assert middle_node(_build([1, 2, 3, 4, 5])).val == 3      # type: ignore[union-attr]
    assert middle_node(_build([1, 2, 3, 4])).val == 3         # type: ignore[union-attr]
    assert middle_node(_build([1])).val == 1                  # type: ignore[union-attr]
    assert middle_node(_build([])) is None

    assert has_cycle(_build([])) is False
    single = ListNode(1)
    single.next = single
    assert has_cycle(single) is True

    tail = _build([1, 2, 3, 4])
    cyclic = ListNode(0, tail)
    node = tail
    for _ in range(3):
        node = node.next  # type: ignore[union-attr]
    node.next = tail           # type: ignore[union-attr]  # замыкаем в цикл
    assert has_cycle(cyclic) is True

    print("All tests passed")
