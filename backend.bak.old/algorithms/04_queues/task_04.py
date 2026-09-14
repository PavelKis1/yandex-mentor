"""Очереди: FIFO-очередь, круговая очередь, максимум скользящего окна."""

from collections import deque


class Queue:
    """FIFO-очередь на collections.deque — O(1) на enqueue/dequeue.

    Edge cases: пустая очередь (dequeue бросает IndexError), один элемент.
    """

    def __init__(self) -> None:
        self._items: deque[int] = deque()

    def enqueue(self, value: int) -> None:
        self._items.append(value)

    def dequeue(self) -> int:
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def is_empty(self) -> bool:
        return not self._items

    def size(self) -> int:
        return len(self._items)


class CircularQueue:
    """Круговая очередь фиксированного размера на кольцевом массиве.

    O(1) на все операции. Edge cases: полная и пустая очередь, capacity = 1.
    """

    def __init__(self, capacity: int) -> None:
        self._data: list[int | None] = [None] * capacity
        self._head = 0
        self._tail = -1
        self._count = 0

    def enqueue(self, value: int) -> bool:
        if self.is_full():
            return False
        self._tail = (self._tail + 1) % len(self._data)
        assert self._data[self._tail] is None
        self._data[self._tail] = value
        self._count += 1
        return True

    def dequeue(self) -> bool:
        if self.is_empty():
            return False
        assert self._data[self._head] is not None
        self._data[self._head] = None
        self._head = (self._head + 1) % len(self._data)
        self._count -= 1
        return True

    def front(self) -> int | None:
        if self.is_empty():
            return None
        return self._data[self._head]

    def rear(self) -> int | None:
        if self.is_empty():
            return None
        return self._data[self._tail]

    def is_empty(self) -> bool:
        return self._count == 0

    def is_full(self) -> bool:
        return self._count == len(self._data)


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """O(n) — deque индексов; максимум каждого окна размера k.

    Edge cases: пустой массив, k <= 0, k > len(nums) — возвращаем [].
    """
    if not nums or k <= 0 or k > len(nums):
        return []
    result: list[int] = []
    window: deque[int] = deque()
    for i, num in enumerate(nums):
        while window and nums[window[-1]] <= num:
            window.pop()
        window.append(i)
        if window[0] <= i - k:
            window.popleft()
        if i >= k - 1:
            result.append(nums[window[0]])
    return result


if __name__ == "__main__":
    q = Queue()
    assert q.is_empty() is True
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1
    assert q.size() == 1
    assert q.dequeue() == 2
    assert q.is_empty() is True
    try:
        q.dequeue()
        raise AssertionError("dequeue on empty queue must fail")
    except IndexError:
        pass

    cq = CircularQueue(3)
    assert cq.enqueue(1) is True
    assert cq.enqueue(2) is True
    assert cq.enqueue(3) is True
    assert cq.is_full() is True
    assert cq.enqueue(4) is False
    assert cq.front() == 1
    assert cq.rear() == 3
    assert cq.dequeue() is True
    assert cq.enqueue(4) is True
    assert cq.front() == 2
    assert cq.rear() == 4

    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([], 3) == []
    assert max_sliding_window([5, 4, 3], 0) == []
    assert max_sliding_window([1, 2], 5) == []

    print("All tests passed")
