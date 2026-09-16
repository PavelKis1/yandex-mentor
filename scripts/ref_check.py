"""Эталонная проверка тестовых данных авторских задач.

Для каждой задачи из REF, известной реализации, прогоняет все test_cases из
backend/tasks/<lect>/problems/p<k>.json и сверяет полученное значение с expected.
Выводит расхождения.

Запуск: python scripts/ref_check.py
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "backend" / "tasks"

# ----------------------------- эталонные реализации ----------------------- #

def intersection(nums1, nums2):
    return sorted(set(nums1) & set(nums2))

def count_unique(nums):
    return len(set(nums))

def is_subset(small, large):
    from collections import Counter
    cs, cl = Counter(small), Counter(large)
    return all(cs[k] <= cl.get(k, 0) for k in cs)

def is_valid(s):
    st, m = [], {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in m:
            if not st or st[-1] != m[ch]:
                return False
            st.pop()
        else:
            st.append(ch)
    return not st

def eval_rpn(tokens):
    st = []
    for t in tokens:
        if t in "+-*/":
            b, a = st.pop(), st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            else:
                st.append(int(a / b))
        else:
            st.append(int(t))
    return st[0]

def largest_rectangle_area(heights):
    st, best, heights = [], 0, heights + [0]
    for i, h in enumerate(heights):
        while st and heights[st[-1]] > h:
            idx = st.pop()
            left = st[-1] if st else -1
            best = max(best, heights[idx] * (i - left - 1))
        st.append(i)
    return best

def first_unique_char(s):
    from collections import Counter
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1:
            return i
    return -1

def josephus(n, k):
    from collections import deque
    dq = deque(range(1, n + 1))
    while len(dq) > 1:
        dq.rotate(-(k - 1))
        dq.popleft()
    return dq[0]

def max_sliding_window(nums, k):
    from collections import deque
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


# ----------------------------- 26-29: collections/itertools/functools/internals - #
def top_k_frequent(nums, k):
    from collections import Counter
    return [x for x, _ in Counter(nums).most_common(k)]


def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())


def is_palindrome(s):
    from collections import deque
    dq = deque(ch.lower() for ch in s if ch.isalnum())
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True


def combinations(nums, k):
    from itertools import combinations as C
    return [list(c) for c in C(nums, k)]


def cartesian_product(lists):
    from itertools import product
    seen, out = set(), []
    for t in product(*lists):
        tt = tuple(t)
        if tt not in seen:
            seen.add(tt)
            out.append(list(tt))
    return out


def cyclic_sequence(n, count):
    from itertools import cycle, islice
    return list(islice(cycle(range(n)), count))


def discounted_prices(prices, percent):
    return [int(p * (100 - percent) // 100) for p in prices]


def fib(n):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def f(x):
        return x if x < 2 else f(x - 1) + f(x - 2)

    return f(n)


def reduce_max(nums):
    from functools import reduce
    if not nums:
        return None
    return reduce(lambda a, b: a if a > b else b, nums)


def append_unique(lst, value):
    if value not in lst:
        lst.append(value)
        return True
    return False


def closure_counter(steps):
    def make():
        c = 0

        def inc():
            nonlocal c
            c += 1
            return c

        return inc

    fn = make()
    return [fn() for _ in range(steps)]


def first_primes(n):
    def is_prime(x):
        if x < 2:
            return False
        i = 2
        while i * i <= x:
            if x % i == 0:
                return False
            i += 1
        return True

    out, cand = [], 2
    while len(out) < n:
        if is_prime(cand):
            out.append(cand)
        cand += 1
    return out


# ----------- ListNode helpers (для задач на связные списки, 05) ----------- #
class ListNode:
    def __init__(self, v=0, nxt=None):
        self.val = v
        self.next = nxt

def _build(values):
    d = ListNode()
    t = d
    for v in values:
        t.next = ListNode(v)
        t = t.next
    return d.next

def _to_list(head):
    r = []
    while head:
        r.append(head.val)
        head = head.next
    return r

def reverse_list(values):
    head, prev = _build(values), None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return _to_list(prev)

def middle_node(values):
    head = _build(values)
    if head is None:
        return None
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.val


def _build_cyclic(values, pos):
    if not values:
        return None
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    if pos < 0 or pos >= len(values):
        return dummy.next
    node = dummy.next
    for _ in range(pos):
        node = node.next
    tail.next = node
    return dummy.next


def linked_has_cycle(spec):
    values, pos = spec[0], spec[1]
    head = _build_cyclic(values, pos)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# --------------------------- бинарные деревья (06) ------------------------ #
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def _build_bt(level):
    if not level or level[0] is None:
        return None
    root = TreeNode(level[0])
    q, i = [root], 1
    while q and i < len(level):
        node = q.pop(0)
        if i < len(level) and level[i] is not None:
            node.left = TreeNode(level[i])
            q.append(node.left)
        i += 1
        if i < len(level) and level[i] is not None:
            node.right = TreeNode(level[i])
            q.append(node.right)
        i += 1
    return root


def preorder(level):
    root = _build_bt(level)
    out = []

    def rec(node):
        if node is None:
            return
        out.append(node.val)
        rec(node.left)
        rec(node.right)
    rec(root)
    return out


def max_depth(level):
    def rec(node):
        if node is None:
            return 0
        return 1 + max(rec(node.left), rec(node.right))
    return rec(_build_bt(level))


def is_valid_bst(level):
    def rec(node, lo, hi):
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return rec(node.left, lo, node.val) and rec(node.right, node.val, hi)
    return rec(_build_bt(level), float("-inf"), float("inf"))


# ------------------------------- кучи (07) -------------------------------- #
def find_kth_largest(nums, k):
    import heapq
    return heapq.nlargest(k, nums)[-1]


def merge_k_lists(lists):
    import heapq
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return out


def top_k_frequent(nums, k):
    from collections import Counter
    c = Counter(nums)
    return sorted(c, key=lambda x: (-c[x], x))[:k]


# ---------------------- скользящее окно (08) ------------------------------ #
def max_subarray_sum(nums, k):
    if k <= 0 or k > len(nums):
        return None
    window = sum(nums[:k])
    best = window
    for i in range(len(nums) - k):
        window = window - nums[i] + nums[i + k]
        best = max(best, window)
    return best


def length_of_longest_substring(s):
    seen = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


def min_window(s, t):
    from collections import Counter
    if not t:
        return ""
    need = Counter(t)
    formed = 0
    required = len(need)
    win = {}
    left = 0
    ans, ans_len = "", float("inf")
    for right, ch in enumerate(s):
        if ch in need:
            win[ch] = win.get(ch, 0) + 1
            if win[ch] == need[ch]:
                formed += 1
        while formed == required and left <= right:
            if right - left + 1 < ans_len:
                ans_len = right - left + 1
                ans = s[left:right + 1]
            chl = s[left]
            if chl in need:
                win[chl] -= 1
                if win[chl] < need[chl]:
                    formed -= 1
            left += 1
    return ans


# ----------------------------- два указателя (09) -------------------------- #
def two_sum(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [nums[left], nums[right]]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []


def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best


# --------------------------- бинарный поиск (10) --------------------------- #
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:      # левая половина отсортирована
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                            # правая половина отсортирована
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def min_eating_speed(piles, h):
    if not piles:
        return -1
    import math
    need = sum(math.ceil(p / max(piles)) for p in piles)
    if need > h:
        return -1
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(math.ceil(p / mid) for p in piles) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


# --------------------------- префиксные суммы (11) ------------------------- #
def range_sum(nums, l, r):
    P = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        P[i + 1] = P[i] + nums[i]
    return P[r + 1] - P[l]


def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] *= left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out


def count_subarrays(nums, k):
    from collections import defaultdict
    counts = defaultdict(int)
    counts[0] = 1
    cur = total = 0
    for x in nums:
        cur += x
        total += counts[cur - k]
        counts[cur] += 1
    return total


# ------------------------------ жадные (12) -------------------------------- #
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True


def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    total = start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:
            total = 0
            start = i + 1
    return start


def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda x: x[1])
    count = 0
    prev = float("-inf")
    for start, end in intervals:
        if start >= prev:
            prev = end
        else:
            count += 1
    return count


# ------------------------------ DP 1D (13) --------------------------------- #
def climb_stairs(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def rob(nums):
    prev = curr = 0
    for x in nums:
        prev, curr = curr, max(curr, prev + x)
    return curr


def coin_change(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] <= amount else -1


# ------------------------------ DP 2D (14) --------------------------------- #
def unique_paths(m, n):
    if m < 1 or n < 1:
        return 0
    row = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]


def longest_common_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            t = dp[j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = t
    return dp[n]


def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            t = dp[j]
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = t
    return dp[n]


# ---------------------------- DP по строкам (15) --------------------------- #
def longest_palindrome(s):
    if not s:
        return ""
    best = ""
    for i in range(len(s)):
        for lo, hi in ((i, i), (i, i + 1)):
            l, r = lo, hi
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            sub = s[l + 1:r]
            if len(sub) > len(best):
                best = sub
    return best


def word_break(s, word_dict):
    wset = set(word_dict)
    ok = [False] * (len(s) + 1)
    ok[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if ok[j] and s[j:i] in wset:
                ok[i] = True
                break
    return ok[-1]


# ---------------------------- backtracking (16) ---------------------------- #
def permute(nums):
    from itertools import permutations
    return [list(p) for p in permutations(nums)]


def subsets(nums):
    n = len(nums)
    out = [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
    return sorted(out, key=repr)


def solve_n_queens(n):
    res = []
    cols, diag1, diag2 = set(), set(), set()
    def bt(row, board):
        if row == n:
            res.append(list(board))
            return
        for c in range(n):
            if c in cols or (row - c) in diag1 or (row + c) in diag2:
                continue
            cols.add(c); diag1.add(row - c); diag2.add(row + c)
            board.append("." * c + "Q" + "." * (n - c - 1))
            bt(row + 1, board)
            board.pop(); cols.discard(c); diag1.discard(row - c); diag2.discard(row + c)
    bt(0, [])
    return sorted(res, key=repr)


# -------------------------------- BFS (17) --------------------------------- #
def open_lock(deadends, target):
    from collections import deque
    if "0000" in deadends:
        return -1
    dead = set(deadends)
    seen = {"0000"}
    q = deque([("0000", 0)])
    while q:
        cur, d = q.popleft()
        if cur == target:
            return d
        for i in range(4):
            for delta in (1, -1):
                nxt = cur[:i] + str((int(cur[i]) + delta) % 10) + cur[i + 1:]
                if nxt not in seen and nxt not in dead:
                    seen.add(nxt)
                    q.append((nxt, d + 1))
    return -1


def oranges_rotting(grid):
    from collections import deque
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    mins = 0
    while q:
        r, c, t = q.popleft()
        mins = t
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return mins if fresh == 0 else -1


def shortest_path(graph, start, end):
    from collections import deque
    if start == end:
        return 0
    g = {int(k): list(v) for k, v in graph.items()}
    seen = {start}
    q = deque([(start, 0)])
    while q:
        node, d = q.popleft()
        for nb in g.get(node, []):
            if nb in seen:
                continue
            if nb == end:
                return d + 1
            seen.add(nb)
            q.append((nb, d + 1))
    return -1


# -------------------------------- DFS (18) --------------------------------- #
def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1:
                count += 1
                st = [(r, c)]
                grid[r][c] = 0
                while st:
                    x, y = st.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 1:
                            grid[nx][ny] = 0
                            st.append((nx, ny))
    return count


def max_area_of_island(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    best = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1:
                area = 0
                st = [(r, c)]
                grid[r][c] = 0
                while st:
                    x, y = st.pop()
                    area += 1
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == 1:
                            grid[nx][ny] = 0
                            st.append((nx, ny))
                best = max(best, area)
    return best


def can_finish(num_courses, prerequisites):
    g = {i: [] for i in range(num_courses)}
    for a, b in prerequisites:
        g[b].append(a)
    state = [0] * num_courses
    def dfs(u):
        state[u] = 1
        for v in g[u]:
            if state[v] == 1:
                return False
            if state[v] == 0 and not dfs(v):
                return False
        state[u] = 2
        return True
    return all(dfs(i) for i in range(num_courses) if state[i] == 0)


# ---------------------------- топосорт (19) -------------------------------- #
def topological_sort(graph, n):
    from collections import deque
    g = {}
    indeg = [0] * n
    for k, v in graph.items():
        k = int(k)
        g[k] = [int(x) for x in v]
        for x in g[k]:
            indeg[x] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    res = []
    while q:
        u = q.popleft()
        res.append(u)
        for v in g.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return res if len(res) == n else []


def has_cycle(graph, n):
    g = {}
    for k, v in graph.items():
        k = int(k)
        g[k] = [int(x) for x in v]
    state = [0] * n
    def dfs(u):
        state[u] = 1
        for v in g.get(u, []):
            if state[v] == 1:
                return True
            if state[v] == 0 and dfs(v):
                return True
        state[u] = 2
        return False
    return any(dfs(i) for i in range(n) if state[i] == 0)


def alien_order(words):
    ch = set("".join(words))
    for a, b in zip(words, words[1:]):
        if a.startswith(b) and a != b:
            return ""
    g = {c: set() for c in ch}
    indeg = {c: 0 for c in ch}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in g[x]:
                    g[x].add(y)
                    indeg[y] += 1
                break
    from collections import deque
    q = deque(sorted(c for c in ch if indeg[c] == 0))
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in sorted(g[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return "".join(out) if len(out) == len(ch) else ""


# --------------------------- union-find (20) ------------------------------- #
def find_circle_num(is_connected):
    if not is_connected:
        return 0
    n = len(is_connected)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for i in range(n):
        for j in range(n):
            if is_connected[i][j]:
                pi, pj = find(i), find(j)
                if pi != pj:
                    parent[pj] = pi
    return len({find(i) for i in range(n)})


def find_redundant_connection(edges):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        pa, pb = find(a), find(b)
        if pa == pb:
            return [a, b]
        parent[pb] = pa
    return []


def accounts_merge(accounts):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        pa, pb = find(a), find(b)
        if pa != pb:
            parent[pb] = pa
    owner = {}
    for acc in accounts:
        name = acc[0]
        for em in acc[1:]:
            owner[em] = name
            if len(acc) > 1:
                union(acc[1], em)
    groups = {}
    for em in owner:
        groups.setdefault(find(em), set()).add(em)
    items = sorted([(sorted(gs)[0], r) for r, gs in groups.items()])
    return [[owner[r]] + sorted(groups[r]) for _, r in items]


# --------------------------------- trie (21) ------------------------------- #
def find_words(board, words):
    if not board or not board[0]:
        return []
    R, C = len(board), len(board[0])
    trie = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["#"] = True
    res = set()
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    def dfs(r, c, node, pre):
        ch = board[r][c]
        if ch not in node:
            return
        node = node[ch]
        if node.get("#"):
            res.add(pre + ch)
        board[r][c] = "*"
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] != "*":
                dfs(nr, nc, node, pre + ch)
        board[r][c] = ch
    for r in range(R):
        for c in range(C):
            dfs(r, c, trie, "")
    return sorted(res)


def replace_words(dictionary, sentence):
    roots = set(dictionary)
    out = []
    for w in sentence.split():
        pre = ""
        replaced = False
        for ch in w:
            pre += ch
            if pre in roots:
                out.append(pre)
                replaced = True
                break
        if not replaced:
            out.append(w)
    return " ".join(out)


def find_max_xor(nums):
    best = mask = 0
    for i in range(31, -1, -1):
        mask |= 1 << i
        pref = {x & mask for x in nums}
        cand = best | (1 << i)
        if any((p ^ cand) in pref for p in pref):
            best = cand
    return best


# ------------------------------ dijkstra (22) ------------------------------ #
def network_delay_time(times, n, k):
    import heapq
    g = {i: [] for i in range(1, n + 1)}
    for u, v, w in times:
        g[u].append((v, w))
    dist = [float("inf")] * (n + 1)
    dist[k] = 0
    pq = [(0, k)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    mx = max(dist[1:])
    return mx if mx < float("inf") else -1


def find_cheapest_price(n, flights, src, dst, k):
    price = [float("inf")] * n
    price[src] = 0
    for _ in range(k + 1):
        nxt = price[:]
        for u, v, p in flights:
            if price[u] != float("inf") and price[u] + p < nxt[v]:
                nxt[v] = price[u] + p
        price = nxt
    return price[dst] if price[dst] < float("inf") else -1


def max_probability(n, edges, succ_prob, start, end):
    import heapq
    g = {i: [] for i in range(n)}
    for (u, v), p in zip(edges, succ_prob):
        g[u].append((v, p))
        g[v].append((u, p))
    prob = [0.0] * n
    prob[start] = 1.0
    pq = [(-1.0, start)]
    while pq:
        negp, u = heapq.heappop(pq)
        p = -negp
        if p < prob[u]:
            continue
        for v, w in g[u]:
            if p * w > prob[v]:
                prob[v] = p * w
                heapq.heappush(pq, (-prob[v], v))
    return prob[end]


# ----------------------------- побитовые (23) ------------------------------ #
def single_number(nums):
    x = 0
    for n in nums:
        x ^= n
    return x


def count_bits(n):
    out = [0] * (n + 1)
    for i in range(1, n + 1):
        out[i] = out[i >> 1] + (i & 1)
    return out


def get_sum(a, b):
    # 32-битное сложение через XOR (сумма) и AND<<1 (перенос);
    # маскирование нужно, чтобы отрицательные числа не давали бесконечный цикл.
    MASK = 0xFFFFFFFF
    while b:
        carry = ((a & b) << 1) & MASK
        a = (a ^ b) & MASK
        b = carry
    if a > 0x7FFFFFFF:
        return a - 0x100000000
    return a


# ------------------------------ строки (24) -------------------------------- #
def is_anagram(s, t):
    from collections import Counter
    return Counter(s) == Counter(t)


def group_anagrams(strs):
    from collections import defaultdict
    d = defaultdict(list)
    for s in strs:
        d["".join(sorted(s))].append(s)
    return [v for v in d.values()]


def length_of_longest_substring(s):
    seen = {}
    left = best = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = i
        best = max(best, i - left + 1)
    return best


# ------------------------- комбинаторика (25) ------------------------------ #
def combine(n, k):
    from itertools import combinations
    return [list(c) for c in combinations(range(1, n + 1), k)]


# ----------------------- сопоставление taskId -> function ----------------- #
REF = {
    "02-p1": intersection,
    "02-p2": count_unique,
    "02-p3": is_subset,
    "03-p1": is_valid,
    "03-p2": eval_rpn,
    "03-p3": largest_rectangle_area,
    "04-p1": first_unique_char,
    "04-p2": josephus,
    "04-p3": max_sliding_window,
    "05-p1": reverse_list,
    "05-p2": middle_node,
    "05-p3": linked_has_cycle,
    "06-p1": preorder,
    "06-p2": max_depth,
    "06-p3": is_valid_bst,
    "07-p1": find_kth_largest,
    "07-p2": merge_k_lists,
    "07-p3": top_k_frequent,
    "08-p1": max_subarray_sum,
    "08-p2": length_of_longest_substring,
    "08-p3": min_window,
    "09-p1": two_sum,
    "09-p2": remove_duplicates,
    "09-p3": max_area,
    "10-p1": binary_search,
    "10-p2": search_rotated,
    "10-p3": min_eating_speed,
    "11-p1": range_sum,
    "11-p2": product_except_self,
    "11-p3": count_subarrays,
    "12-p1": can_jump,
    "12-p2": can_complete_circuit,
    "12-p3": erase_overlap_intervals,
    "13-p1": climb_stairs,
    "13-p2": rob,
    "13-p3": coin_change,
    "14-p1": unique_paths,
    "14-p2": longest_common_subsequence,
    "14-p3": edit_distance,
    "15-p1": longest_palindrome,
    "15-p2": word_break,
    "15-p3": edit_distance,
    "16-p1": permute,
    "16-p2": subsets,
    "16-p3": solve_n_queens,
    "17-p1": open_lock,
    "17-p2": oranges_rotting,
    "17-p3": shortest_path,
    "18-p1": num_islands,
    "18-p2": max_area_of_island,
    "18-p3": can_finish,
    "19-p1": topological_sort,
    "19-p2": has_cycle,
    "19-p3": alien_order,
    "20-p1": find_circle_num,
    "20-p2": find_redundant_connection,
    "20-p3": accounts_merge,
    "21-p1": find_words,
    "21-p2": replace_words,
    "21-p3": find_max_xor,
    "22-p1": network_delay_time,
    "22-p2": find_cheapest_price,
    "22-p3": max_probability,
    "23-p1": single_number,
    "23-p2": count_bits,
    "23-p3": get_sum,
    "24-p1": is_anagram,
    "24-p2": group_anagrams,
    "24-p3": length_of_longest_substring,
    "25-p1": combine,
    "25-p2": permute,
    "25-p3": subsets,
    "26-p1": top_k_frequent,
    "26-p2": group_anagrams,
    "26-p3": is_palindrome,
    "27-p1": combinations,
    "27-p2": cartesian_product,
    "27-p3": cyclic_sequence,
    "28-p1": discounted_prices,
    "28-p2": fib,
    "28-p3": reduce_max,
    "29-p1": append_unique,
    "29-p2": closure_counter,
    "29-p3": first_primes,
}


def norm(value, sort_result):
    if sort_result and isinstance(value, list):
        return sorted([sorted(g) if isinstance(g, (list, tuple)) else g for g in value], key=repr)
    return value


def main():
    total = 0
    problems_found = 0
    for pdir in sorted(BASE.iterdir()):
        if not pdir.is_dir():
            continue
        pprobs = pdir / "problems"
        if not pprobs.exists():
            continue
        for k in (1, 2, 3):
            pf = pprobs / f"p{k}.json"
            if not pf.exists():
                continue
            data = json.loads(pf.read_text(encoding="utf-8"))
            fn = REF.get(data["id"])
            problems_found += 1
            if fn is None:
                continue
            for tc in data["test_cases"]:
                total += 1
                got = norm(fn(*tc["args"]), tc.get("sort_result", False))
                exp = norm(tc["expected"], tc.get("sort_result", False))
                status = "OK" if got == exp else "MISMATCH"
                if status != "OK":
                    print(f"[{status}] {data['id']}/{tc['id']}: got={got!r} expected={exp!r}")
    print(f"Проверено задач: {problems_found}, тест-кейсов с эталоном: {total}")

if __name__ == "__main__":
    main()