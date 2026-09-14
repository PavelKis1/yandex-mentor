"""Проверка синтаксиса всех task_*.py в backend/ (разовая утилита)."""
import pathlib
import py_compile

bad = []
files = sorted(pathlib.Path("backend").rglob("task_*.py"))
print(f"found: {len(files)} file(s)")
for f in files:
    try:
        py_compile.compile(str(f), doraise=True)
    except py_compile.PyCompileError as exc:
        bad.append(str(exc))

if bad:
    print("SYNTAX ERRORS:")
    print("\n".join(bad))
    raise SystemExit(1)
print("OK: все файлы проходят py_compile")