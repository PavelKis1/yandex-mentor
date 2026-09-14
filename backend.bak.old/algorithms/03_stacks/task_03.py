"""Стеки: валидные скобки, MinStack, обратная польская нотация."""

import operator


def is_valid(s: str) -> bool:
    """O(n) — стек открывающих скобок, закрывающая должна совпадать с верхушкой.

    Edge cases: пустая строка, только открывающие, только закрывающие скобки.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack


class MinStack:
    """O(1) на push/pop/top/get_min — храним пару (значение, текущий минимум).

    Edge cases: пустой стек, повторяющиеся минимальные значения.
    """

    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def get_min(self) -> int:
        return self._stack[-1][1]


def eval_rpn(tokens: list[str]) -> int:
    """O(n) — стек операндов; операторы +, -, *, / (деление с усечением к нулю).

    Edge cases: один токен без операторов, отрицательные операнды,
    деление, дающее дробный результат.
    """
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": lambda a, b: int(a / b),
    }
    stack: list[int] = []
    for token in tokens:
        if token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    return stack[0]


if __name__ == "__main__":
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("([)]") is False
    assert is_valid("") is True
    assert is_valid("{[]}") is True

    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.get_min() == -2

    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["3", "4", "-"]) == -1

    print("All tests passed")
