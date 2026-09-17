import json
from pathlib import Path

tasks_dir = Path("backend/tasks")
for i in range(50, 60):
    folder = next(tasks_dir.glob(f"{i}_*"))
    problems_dir = folder / "problems"
    print(f"--- {folder.name} ---")
    for prob_file in problems_dir.glob("*.json"):
        with open(prob_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"{data.get('id')}: {data.get('title')}")
