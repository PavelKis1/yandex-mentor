"""Тесты чекера: изолированный subprocess-запуск решений и вердикты."""
from src import config
from src.core.checker import run_checks
from src.core.registry import Problem, TestCase

TestCase.__test__ = False  # дата-класс реестра, а не pytest-класс

TWO_SUM = Problem(
    id="t-p1",
    title="Two Sum",
    difficulty="easy",
    lecture_id="t",
    order=1,
    description="two sum",
    entry_function="two_sum",
    test_cases=[
        TestCase(id="t1", args=[[2, 7, 11, 15], 9], expected=[0, 1], hidden=False),
        TestCase(id="t2", args=[[3, 2, 4], 6], expected=[1, 2], hidden=False),
        TestCase(id="t3", args=[[3, 3], 6], expected=[0, 1], hidden=True),
    ],
    timeout_ms=3000,
)

GOOD = """\
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        c = target - x
        if c in seen:
            return [seen[c], i]
        seen[x] = i
    return []
"""


def _isolate(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "SOLUTIONS_DIR", tmp_path)
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)


def test_accepted(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(TWO_SUM, GOOD, hide_hidden=False)
    assert result["verdict"] == "accepted"
    assert len(result["results"]) == 3
    assert all(r["passed"] for r in result["results"])


def test_hidden_tests_excluded_from_run(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(TWO_SUM, GOOD, hide_hidden=True)
    assert result["verdict"] == "accepted"
    assert len(result["results"]) == 2  # скрытый t3 не выполняется


def test_wrong_answer(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(TWO_SUM, "def two_sum(nums, target):\n    return [0, 0]\n", hide_hidden=False)
    assert result["verdict"] == "wrong_answer"
    assert any(not r["passed"] for r in result["results"])


def test_syntax_error(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(TWO_SUM, "def two_sum(nums, target:\n    pass\n", hide_hidden=False)
    assert result["verdict"] == "syntax_error"
    assert "SyntaxError" in (result.get("error") or "")


def test_runtime_error(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    code = "def two_sum(nums, target):\n    return undefined_name\n"
    result = run_checks(TWO_SUM, code, hide_hidden=False)
    assert result["verdict"] == "runtime_error"
    assert any("NameError" in (r["error"] or "") for r in result["results"])


def test_timeout(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    slow = Problem(
        id="t-slow",
        title="slow",
        difficulty="easy",
        lecture_id="t",
        order=1,
        description="slow",
        entry_function="spinner",
        test_cases=[TestCase(id="t1", args=[[1]], expected=1, hidden=False)],
        timeout_ms=200,
    )
    code = "def spinner(x):\n    while True:\n        pass\n"
    monkeypatch.setattr("src.core.checker._STARTUP_SLACK_SEC", 0.3)
    result = run_checks(slow, code, hide_hidden=False)
    assert result["verdict"] == "timeout"


def test_no_tests(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    empty = Problem(
        id="t-empty",
        title="empty",
        difficulty="easy",
        lecture_id="t",
        order=1,
        description="empty",
        entry_function=None,
        test_cases=[],
        timeout_ms=3000,
    )
    result = run_checks(empty, "anything", hide_hidden=False)
    assert result["verdict"] == "no_tests"


def test_converters_and_sort_result(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    problem = Problem(
        id="t-ll",
        title="linked",
        difficulty="medium",
        lecture_id="t",
        order=1,
        description="linked list",
        entry_function="reverse_list",
        test_cases=[
            TestCase(
                id="t1",
                args=[[1, 2, 3]],
                expected=[3, 2, 1],
                arg_converters=["_build"],
                result_converter="_to_list",
            )
        ],
        timeout_ms=3000,
    )
    code = """\
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def _build(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def _to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out

def reverse_list(head):
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
"""
    result = run_checks(problem, code, hide_hidden=False)
    assert result["verdict"] == "accepted"

    # sort_result: группы анаграмм в любом порядке
    anagram = Problem(
        id="t-an",
        title="anagrams",
        difficulty="medium",
        lecture_id="t",
        order=1,
        description="anagrams",
        entry_function="group",
        test_cases=[
            TestCase(
                id="t1",
                args=[["eat", "tea", "tan", "ate", "nat", "bat"]],
                expected=[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]],
                sort_result=True,
            )
        ],
        timeout_ms=3000,
    )
    code_an = """\
def group(strs):
    table = {}
    for s in strs:
        table.setdefault(tuple(sorted(s)), []).append(s)
    return list(table.values())
"""
    result = run_checks(anagram, code_an, hide_hidden=False)
    assert result["verdict"] == "accepted"


SQL_PROBLEM = Problem(
    id="t-sql",
    title="SQL select",
    difficulty="easy",
    lecture_id="t",
    order=1,
    description="select adults",
    language="sql",
    entry_function=None,
    test_cases=[
        TestCase(
            id="t1",
            args=[],
            expected=[["Alice", 30], ["Bob", 25]],
            hidden=False,
            db_schema=(
                "CREATE TABLE users(id INTEGER, name TEXT, age INTEGER);\n"
                "INSERT INTO users VALUES (1, 'Alice', 30);\n"
                "INSERT INTO users VALUES (2, 'Bob', 25);\n"
                "INSERT INTO users VALUES (3, 'Kid', 10);"
            ),
        ),
        TestCase(
            id="t2",
            args=[],
            expected=[["Bob", 25]],
            hidden=True,
            db_schema=(
                "CREATE TABLE users(id INTEGER, name TEXT, age INTEGER);\n"
                "INSERT INTO users VALUES (1, 'Bob', 25);\n"
                "INSERT INTO users VALUES (3, 'Kid', 10);"
            ),
        ),
    ],
    timeout_ms=3000,
)


def test_sql_accepted(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(
        SQL_PROBLEM,
        "SELECT name, age FROM users WHERE age >= 18 ORDER BY age;",
        hide_hidden=False,
    )
    assert result["verdict"] == "accepted"
    assert all(r["passed"] for r in result["results"])


def test_sql_wrong_answer(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    result = run_checks(
        SQL_PROBLEM,
        "SELECT name FROM users;",
        hide_hidden=False,
    )
    assert result["verdict"] == "wrong_answer"
    assert any(not r["passed"] for r in result["results"])


def test_sql_rows_unordered(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    # Порядок строк не должен влиять на вердикт (сравнение как мультимножества).
    result = run_checks(
        SQL_PROBLEM,
        "SELECT name, age FROM users WHERE age >= 18;",
        hide_hidden=False,
    )
    assert result["verdict"] == "accepted"