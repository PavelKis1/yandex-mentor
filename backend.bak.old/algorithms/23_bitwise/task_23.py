"""Битовая арифметика: одинокий элемент, подсчёт бит, сумма без «+» и «-»."""


def single_number(nums: list[int]) -> int:
    """O(n) — XOR всех элементов; дубликаты попарно уничтожаются.

    Edge cases: один элемент, все пары, отрицательные числа.
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def count_bits(n: int) -> list[int]:
    """O(n) — по элементам: count[i] = count[i >> 1] + (i & 1).

    Edge cases: n = 0 ([0]), n = 1, большие n.
    """
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result


def get_sum(a: int, b: int) -> int:
    """O(1) — сложение через XOR (сумма) + сдвинутый AND (перенос).

    Edge cases: оба ноля (0), разные знаки, оба отрицательных,
    результат, выходящий за 32-битный знаковый диапазон.
    """
    mask = 0xFFFFFFFF
    while b:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    return a if a <= 0x7FFFFFFF else a - (1 << 32)


if __name__ == "__main__":
    assert single_number([2, 2, 1]) == 1
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1

    assert count_bits(0) == [0]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]

    assert get_sum(1, 2) == 3
    assert get_sum(2, 3) == 5
    assert get_sum(0, 0) == 0
    assert get_sum(-1, 1) == 0
    assert get_sum(-2, -3) == -5

    print("All tests passed")
