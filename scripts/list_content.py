"""Каталоги контента backend/: наличие task.md / task_*.py / lecture.md."""
import pathlib

root = pathlib.Path("backend")
for cat in sorted([d for d in root.iterdir() if d.is_dir()]):
    print(f"\n### {cat.name}/ ({len(list(cat.iterdir()))} тем)")
    for theme in sorted([d for d in cat.iterdir() if d.is_dir()]):
        files = [p.name for p in sorted(theme.iterdir())]
        py_tasks = sorted(p.name for p in theme.glob("task_*.py"))
        marks = []
        marks.append("md" if "task.md" in files else "--")
        marks.append("py" if py_tasks else "--")
        print(f"  {theme.name:<40} task.md={marks[0]} py={','.join(py_tasks) or marks[1]} files={','.join(files)}")