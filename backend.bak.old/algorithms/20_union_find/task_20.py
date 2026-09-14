"""Union-Find: провинции, лишнее ребро, объединение аккаунтов."""


def find_circle_num(is_connected: list[list[int]]) -> int:
    """O(n^2 α(n)) — число компонент связности по матрице смежности.

    Edge cases: n = 0, одна провинция, изолированные вершины.
    """
    n = len(is_connected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    provinces = n
    for i in range(n):
        for j in range(i + 1, n):
            if is_connected[i][j]:
                root_i, root_j = find(i), find(j)
                if root_i != root_j:
                    parent[root_i] = root_j
                    provinces -= 1
    return provinces


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """O(n α(n)) — первое ребро, замыкающее цикл; без цикла — [].

    Edge cases: нет цикла, цикл из двух вершин, ребро-петля.
    """
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_u] = root_v
    return []


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """O(N log N) — DSU по email; результат: имя + отсортированные email.

    Edge cases: один email в аккаунте, дубликаты email, несколько аккаунтов
    одного человека, соединяющиеся через общий email.
    """
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        root_a, root_b = find(a), find(b)
        if root_a != root_b:
            parent[root_a] = root_b

    email_to_name: dict[str, str] = {}
    for account in accounts:
        first_email = account[1]
        for email in account[1:]:
            email_to_name[email] = account[0]
            union(first_email, email)

    groups: dict[str, list[str]] = {}
    for email in email_to_name:
        groups.setdefault(find(email), []).append(email)
    return [[email_to_name[root], *sorted(emails)] for root, emails in groups.items()]


if __name__ == "__main__":
    assert find_circle_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert find_circle_num([[1]]) == 1
    assert find_circle_num([]) == 0
    assert find_circle_num([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    assert find_redundant_connection([]) == []

    merged = sorted(
        accounts_merge(
            [
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                ["John", "johnsmith@mail.com", "john00@mail.com"],
                ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"],
            ]
        )
    )
    assert merged == [
        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
        ["John", "johnnybravo@mail.com"],
        ["Mary", "mary@mail.com"],
    ]

    print("All tests passed")
