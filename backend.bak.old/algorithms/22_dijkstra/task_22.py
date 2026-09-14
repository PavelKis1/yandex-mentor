"""Дейкстра: сетевая задержка, дешёвые рейсы, максимальная вероятность."""

import heapq


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """O((V+E) log V) — время, за которое сигнал дойдёт до всех узлов.

    Edge cases: n = 0 (0), недостижимые узлы (-1), один узел (0).
    """
    graph: dict[int, list[tuple[int, int]]] = {}
    for u, v, w in times:
        graph.setdefault(u, []).append((v, w))
    dist: dict[int, int] = {k: 0}
    heap: list[tuple[int, int]] = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        for neighbor, weight in graph.get(node, []):
            nd = d + weight
            if nd < dist.get(neighbor, float("inf")):
                dist[neighbor] = nd
                heapq.heappush(heap, (nd, neighbor))
    return max(dist.values()) if len(dist) == n else -1


def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """O(k * E * log V) — Дейкстра + лимит k промежуточных остановок.

    Edge cases: src == dst (0), нет маршрута (-1), k = 0 (только напрямую).
    """
    graph: dict[int, list[tuple[int, int]]] = {}
    for u, v, w in flights:
        graph.setdefault(u, []).append((v, w))
    heap: list[tuple[int, int, int]] = [(0, src, 0)]  # cost, node, stops_used
    best: dict[tuple[int, int], int] = {}  # (node, stops) -> min cost
    while heap:
        cost, node, stops = heapq.heappop(heap)
        if node == dst:
            return cost
        if stops > k:
            continue
        for neighbor, weight in graph.get(node, []):
            key = (neighbor, stops + 1)
            new_cost = cost + weight
            if key not in best or new_cost < best[key]:
                best[key] = new_cost
                heapq.heappush(heap, (new_cost, neighbor, stops + 1))
    return -1


def max_probability(
    n: int,
    edges: list[list[int]],
    succ_prob: list[float],
    start: int,
    end: int,
) -> float:
    """O((V+E) log V) — путь с максимальной вероятностью (неориентированный).

    Edge cases: start == end (1.0), нет пути (0.0), ноль узлов.
    """
    graph: dict[int, list[tuple[int, float]]] = {}
    for (a, b), p in zip(edges, succ_prob):
        graph.setdefault(a, []).append((b, p))
        graph.setdefault(b, []).append((a, p))
    prob: dict[int, float] = {start: 1.0}
    heap: list[tuple[float, int]] = [(-1.0, start)]
    while heap:
        neg_p, node = heapq.heappop(heap)
        p = -neg_p
        if p < prob.get(node, 0.0):
            continue
        for neighbor, edge_p in graph.get(node, []):
            np = p * edge_p
            if np > prob.get(neighbor, 0.0):
                prob[neighbor] = np
                heapq.heappush(heap, (-np, neighbor))
    return prob.get(end, 0.0)


if __name__ == "__main__":
    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 1) == 1
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1

    assert (
        find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1)
        == 200
    )
    assert (
        find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0)
        == 500
    )
    assert find_cheapest_price(3, [[0, 1, 100]], 0, 2, 1) == -1
    assert find_cheapest_price(3, [], 1, 1, 0) == 0

    assert abs(max_probability(3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2) - 0.25) < 1e-9
    assert abs(max_probability(2, [[0, 1]], [0.5], 0, 0) - 1.0) < 1e-9
    assert max_probability(3, [[0, 1]], [0.5], 0, 2) == 0.0

    print("All tests passed")
