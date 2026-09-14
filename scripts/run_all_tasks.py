"""Прогоняет все task_*.py файлы как отдельные процессы и печатает итог."""

import glob
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    files = sorted(glob.glob(str(ROOT / "backend" / "algorithms" / "*" / "task_*.py")))
    failed = []
    for path in files:
        result = subprocess.run(
            [sys.executable, path], capture_output=True, text=True
        )
        status = "OK " if result.returncode == 0 else "FAIL"
        print(f"[{status}] {Path(path).relative_to(ROOT)}")
        if result.returncode != 0:
            failed.append(path)
            print(result.stdout, result.stderr, sep="\n")
    print(f"\nTotal: {len(files)}, failed: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())