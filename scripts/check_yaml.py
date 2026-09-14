"""Валидация YAML-конфигов проекта (CI, и т.п.)."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed — skipping", file=sys.stderr)
    sys.exit(0)

for path in Path(".github").rglob("*.yml"):
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        print(f"yaml ok: {path} jobs={list(data.get('jobs', {}).keys()) if isinstance(data, dict) else 'n/a'}")
    except yaml.YAMLError as exc:
        print(f"yaml FAIL: {path}: {exc}", file=sys.stderr)
        sys.exit(1)