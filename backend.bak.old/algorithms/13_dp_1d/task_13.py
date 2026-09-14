"""DP 1D: лестница, грабитель, монеты."""


def climb_stairs(n: int) -> int:
    """O(n) — фибоначчи: ways(i) = ways(i-1) + ways(i-2).

    Edge cases: n < 0 (0), n = 1 (1 способ), n = 2 (2 способа).
    """
    if n <= 0:
        return 0
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(2, n):
        a, b = b, a + b
    return b


def rob(nums: list[int]) -> int:
    """O(n) — на каждом доме: ограбить (prev + num) или пропустить (curr).

    Edge cases: пустой массив (0), один дом, два дома, чередование.
    """
    prev, curr = 0, 0
    for num in nums:
        prev, curr = curr, max(curr, prev + num)
    return curr


def coin_change(coins: list[int], amount: int) -> int:
    """O(amount * len(coins)) — DP по сумме, инициализация +∞.

    Edge cases: amount = 0 (нужно 0 монет), один номинал,
    невозможно составить сумму (−1).
    """
    INF = float("inf")
    dp = [0] + [INF] * amount
    for coin in coins:
        for s in range(coin, amount + 1):
            dp[s] = min(dp[s], dp[s - coin] + 1)
    return int(dp[amount]) if dp[amount] != INF else -1


if __name__ == "__main__":
    assert climb_stairs(1) == 1
    assert climb_stairs(2) == 2
    assert climb_stairs(4) == 5
    assert climb_stairs(0) == 0
    assert climb_stairs(-3) == 0

    assert rob([]) == 0
    assert rob([5]) == 5
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([2, 1, 1, 2]) == 4
    assert rob([1, 2]) == 2

    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    assert coin_change([1, 5, 10, 25], 30) == 2
    assert coin_change([2], 1) == -1

    print("All tests passed")
