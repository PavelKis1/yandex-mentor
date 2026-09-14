"""Финальная проверка через API: refresh, ревью алгоритмических задач.

Печатает issues по задачам 01–25 (алгоритмы). Выход 0, если у всех ноль.
Не требует внешних зависимостей (urllib).
"""
import json
import time
import urllib.request

BASE = "http://127.0.0.1:8000"
ALGORITHMS_RANGE = range(1, 26)


def http_json(method: str, path: str) -> dict:
    req = urllib.request.Request(BASE + path, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    for _ in range(15):
        try:
            http_json("GET", "/api/progress")
            break
        except OSError:
            time.sleep(2)
    else:
        print("Server is not available on", BASE)
        return 1

    result = http_json("POST", "/api/refresh")
    print(
        "refresh:", result.get("total"), "topics,",
        result.get("complete"), "complete,",
        result.get("issues_count"), "issues total",
    )

    bad: list[str] = []
    for num in ALGORITHMS_RANGE:
        task_id = f"{num:02d}"
        review = http_json("GET", f"/api/task/{task_id}/review")
        issues = review["metrics"].get("issues", [])
        status = "OK  " if not issues else "FAIL"
        print(f"[{status}] {task_id} {review['name']}: {issues}")
        if issues:
            bad.append(task_id)
    print("\nAlgorithms with issues:", bad if bad else "none — all clean")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())