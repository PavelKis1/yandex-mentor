path = 'scripts/ref_check.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Находим REF = {
ref_idx = -1
for i, line in enumerate(lines):
    if 'REF = {' in line:
        ref_idx = i
        break

if ref_idx == -1:
    print("REF = { not found")
    exit(1)

# 2. Новые функции
new_funcs = [
    "\n# ----------------------------- 45-47: REST/FastAPI/SQLAlchemy - #\n",
    "def parse_url_params(url):\n",
    "    from urllib.parse import urlparse, parse_qs\n",
    "    parsed = urlparse(url)\n",
    "    return {k: v[0] for k, v in parse_qs(parsed.query).items()}\n\n",
    "def rest_method_for(action):\n",
    "    mapping = {\"create\": \"POST\", \"read\": \"GET\", \"update\": \"PUT\", \"delete\": \"DELETE\"}\n",
    "    return mapping.get(action.lower())\n\n",
    "def is_valid_rest_uri(uri):\n",
    "    import re\n",
    "    return bool(re.match(r'^/[a-z]+(/[a-z0-9]+)?$', uri))\n\n",
    "def fastapi_route_match(route, path):\n",
    "    import re\n",
    "    pattern = re.sub(r'\{[a-z]+\}', r'[a-z0-9]+', route)\n",
    "    return bool(re.match(f'^{pattern}$', path))\n\n",
    "def validate_pydantic_model(data, schema):\n",
    "    for k, v_type in schema.items():\n",
    "        if k not in data or not isinstance(data[k], v_type):\n",
    "            return False\n",
    "    return True\n\n",
    "def dependency_injection_order(dependencies):\n",
    "    return sorted(dependencies, key=lambda x: x[1])\n\n",
    "def session_commit_behavior(is_active, has_changes):\n",
    "    return is_active and has_changes\n\n",
    "def relationship_load_type(query_type):\n",
    "    return \"joined\" if query_type == \"eager\" else \"lazy\"\n\n",
    "def model_to_dict(obj):\n",
    "    return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}\n\n",
    "\n# ----------------------------- 48-49: Docker/Compose - #\n",
    "def dockerfile_layer_count(commands):\n",
    "    return sum(1 for c in commands if c.split()[0] in [\"RUN\", \"COPY\", \"ADD\"])\n\n",
    "def docker_ignore_pattern(file, patterns):\n",
    "    import fnmatch\n",
    "    return any(fnmatch.fnmatch(file, p) for p in patterns)\n\n",
    "def image_tag_valid(tag):\n",
    "    import re\n",
    "    return bool(re.match(r'^[a-z0-9._-]+$', tag))\n\n",
    "def compose_service_dependency(services):\n",
    "    order = []\n",
    "    def visit(s):\n",
    "        for dep in services.get(s, {}).get('depends_on', []):\n",
    "            if dep not in order: visit(dep)\n",
    "        if s not in order: order.append(s)\n",
    "    for s in services: visit(s)\n",
    "    return order\n\n",
    "def compose_network_mode(config):\n",
    "    return config.get('network_mode', 'bridge')\n\n",
    "def compose_volume_mapping(mapping):\n",
    "    return \":\" in mapping\n\n"
]

# Вставляем функции перед REF = {
# ref_idx - это строка с REF = {, вставляем перед ней.
final_lines = lines[:ref_idx] + new_funcs + lines[ref_idx:]

# 3. Новые задачи в REF
# После вставки функций, ref_idx сместился. Находим REF = { снова.
new_ref_idx = -1
for i, line in enumerate(final_lines):
    if 'REF = {' in line:
        new_ref_idx = i
        break

new_tasks = [
    "    \"45-p1\": parse_url_params,\n",
    "    \"45-p2\": rest_method_for,\n",
    "    \"45-p3\": is_valid_rest_uri,\n",
    "    \"46-p1\": fastapi_route_match,\n",
    "    \"46-p2\": validate_pydantic_model,\n",
    "    \"46-p3\": dependency_injection_order,\n",
    "    \"47-p1\": session_commit_behavior,\n",
    "    \"47-p2\": relationship_load_type,\n",
    "    \"47-p3\": model_to_dict,\n",
    "    \"48-p1\": dockerfile_layer_count,\n",
    "    \"48-p2\": docker_ignore_pattern,\n",
    "    \"48-p3\": image_tag_valid,\n",
    "    \"49-p1\": compose_service_dependency,\n",
    "    \"49-p2\": compose_network_mode,\n",
    "    \"49-p3\": compose_volume_mapping,\n"
]

# Вставляем после REF = { (new_ref_idx + 1)
final_lines = final_lines[:new_ref_idx+1] + new_tasks + final_lines[new_ref_idx+1:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)
print('Applied successfully.')
