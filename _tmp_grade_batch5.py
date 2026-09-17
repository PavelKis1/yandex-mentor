import tempfile
from pathlib import Path
from src import config
from src.core.registry import _parse_problem
from src.core.checker import run_checks

SOLS = {
    "45-p1": "def parse_url_params(url):\n    from urllib.parse import urlparse, parse_qs\n    parsed = urlparse(url)\n    return {k: v[0] for k, v in parse_qs(parsed.query).items()}",
    "45-p2": "def rest_method_for(action):\n    mapping = {'create': 'POST', 'read': 'GET', 'update': 'PUT', 'delete': 'DELETE'}\n    return mapping.get(action.lower())",
    "45-p3": "def is_valid_rest_uri(uri):\n    import re\n    return bool(re.match(r'^/[a-z]+(/[a-z0-9]+)?$', uri))",
    "46-p1": "def fastapi_route_match(route, path):\n    import re\n    pattern = re.sub(r'\\\\{[a-z]+\\\\}', r'[a-z0-9]+', route)\n    return bool(re.match(f'^{pattern}$', path))",
    "46-p2": "def validate_pydantic_model(data, schema):\n    for k, v_type in schema.items():\n        if k not in data or not isinstance(data[k], v_type): return False\n    return True",
    "46-p3": "def dependency_injection_order(dependencies):\n    return sorted(dependencies, key=lambda x: x[1])",
    "47-p1": "def session_commit_behavior(is_active, has_changes):\n    return is_active and has_changes",
    "47-p2": "def relationship_load_type(query_type):\n    return 'joined' if query_type == 'eager' else 'lazy'",
    "47-p3": "def model_to_dict(obj):\n    return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}",
    "48-p1": "def dockerfile_layer_count(commands):\n    return sum(1 for c in commands if c.split()[0] in ['RUN', 'COPY', 'ADD'])",
    "48-p2": "def docker_ignore_pattern(file, patterns):\n    import fnmatch\n    return any(fnmatch.fnmatch(file, p) for p in patterns)",
    "48-p3": "def image_tag_valid(tag):\n    import re\n    return bool(re.match(r'^[a-z0-9._-]+$', tag))",
    "49-p1": "def compose_service_dependency(services):\n    order = []\n    def visit(s):\n        for dep in services.get(s, {}).get('depends_on', []):\n            if dep not in order: visit(dep)\n        if s not in order: order.append(s)\n    for s in services: visit(s)\n    return order",
    "49-p2": "def compose_network_mode(config):\n    return config.get('network_mode', 'bridge')",
    "49-p3": "def compose_volume_mapping(mapping):\n    return ':' in mapping",
}

BASE = Path("backend/tasks")
tmp = tempfile.mkdtemp()
config.SOLUTIONS_DIR = Path(tmp) / "solutions"
config.DATA_DIR = Path(tmp) / "data"
config.SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
config.DATA_DIR.mkdir(parents=True, exist_ok=True)

ok = 0
for pid, code in sorted(SOLS.items()):
    num, pf = pid.split("-")
    order = pf[1:]
    p = next(BASE.glob(f"{num}_*/problems/p{order}.json"))
    prob = _parse_problem(p)
    assert prob, pid
    res = run_checks(prob, code, hide_hidden=False)
    assert res["verdict"] == "accepted", (pid, res["verdict"], res.get("error"))
    ok += 1
print("grader accepted:", ok, "problems")",path: