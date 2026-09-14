"""Live smoke-test: проверка API-цепочек, которые использует фронтенд (вместо браузера)."""
import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8123"


def http_json(method: str, path: str, body: str | None = None) -> dict:
    data = body.encode() if body else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")[:200]
        raise RuntimeError(f"HTTP {err.code}: {detail}") from None


ok = True


def check(name: str, cond: bool, extra: str = "") -> None:
    global ok
    print(("PASS" if cond else "FAIL"), "-", name, extra)
    if not cond:
        ok = False


# 1) roadmap
roadmap = http_json("GET", "/api/roadmap")
stages = roadmap.get("roadmap", [])
total = roadmap.get("total")
check("roadmap has 69 lectures", total == 69, f"total={total}")
check("stages use 'lectures'", all("lectures" in s for s in stages))
first_stage_lectures = stages[0]["lectures"] if stages else []
check("first stage has lectures", len(first_stage_lectures) > 0, f"n={len(first_stage_lectures)}")
lec0 = first_stage_lectures[0] if first_stage_lectures else {"id": "01-hash-tables"}

# 2) progress
progress = http_json("GET", "/api/progress")
check("progress is dict", isinstance(progress, dict))

# 3) lecture data
lecture = http_json("GET", f"/api/lectures/{lec0['id']}")
check("lecture loaded", lecture["id"] == lec0["id"])
problems = lecture.get("problems", [])
check("lecture has problems", len(problems) > 0, f"n={len(problems)}")
p1 = problems[0]
required = ["id", "title", "difficulty", "description", "examples", "constraints",
            "hints", "starter_code", "entry_function", "test_case_count"]
missing = [k for k in required if k not in p1]
check("problem has all public fields", not missing, f"missing={missing}")
check("examples not empty", len(p1["examples"]) > 0)
check("solved flag present", "solved" in p1)

pid = p1["id"]
starter = p1["starter_code"]

# 4) run: непустой код возвращает вердикт с нужной схемой
run_res = http_json("POST", f"/api/tasks/{pid}/run", json.dumps({"code": starter}))
check("run has verdict", run_res.get("verdict") in (
    "accepted", "wrong_answer", "runtime_error", "timeout", "syntax_error", "no_tests"),
    f"verdict={run_res.get('verdict')}")
check("run has results list", isinstance(run_res.get("results"), list))
if run_res.get("results"):
    r0 = run_res["results"][0]
    check("test-result fields", all(k in r0 for k in ("id", "passed")), f"keys={list(r0.keys())}")

# 5) submit непустого кода: схема ответа + task_status (без требования accepted)
sub = http_json("POST", f"/api/tasks/{pid}/submit", json.dumps({"code": starter}))
check("submit schema", sub.get("verdict") in (
    "accepted", "wrong_answer", "runtime_error", "timeout", "syntax_error", "no_tests")
    and sub.get("task_status") in ("todo", "wip", "done")
    and sub.get("lecture_id") == lec0["id"],
    f"verdict={sub.get('verdict')}, status={sub.get('task_status')}")

# 6) code: сохранение черновика
saved = http_json("POST", f"/api/tasks/{pid}/code", json.dumps({"code": starter}))
check("save code", saved.get("status") == "saved", f"resp={saved}")

print("RESULT:", "ALL OK" if ok else "FAILURES")