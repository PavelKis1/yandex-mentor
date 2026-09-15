import os

def apply_template(template_name, target_path):
    template_path = os.path.join(r'c:\Users\Pavel\Desktop\yandex_review\scripts\archive\lecture_templates', template_name)
    if not os.path.exists(template_path):
        print(f'Template not found: {template_path}')
        return
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Applied {template_name} to {target_path}')
    except Exception as e:
        print(f'Failed to apply to {target_path}: {e}')

# Mapping of templates to target files
mapping = {
    '11_prefix_sum.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\11_prefix_sum\lecture.md',
    '12_greedy.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\12_greedy\lecture.md',
    '13_dp_1d.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\13_dp_1d\lecture.md',
    '14_dp_2d.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\14_dp_2d\lecture.md',
    '15_dp_strings.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\15_dp_strings\lecture.md',
    '16_backtracking.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\16_backtracking\lecture.md',
    '17_bfs.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\17_bfs\lecture.md',
    '18_dfs.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\18_dfs\lecture.md',
    '19_toposort.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\19_toposort\lecture.md',
    '20_union_find.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\20_union_find\lecture.md',
    '21_trie.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\21_trie\lecture.md',
    '22_dijkstra.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\22_dijkstra\lecture.md',
    '23_bitwise.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\23_bitwise\lecture.md',
    '24_strings.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\24_strings\lecture.md',
    '25_combinations.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\algorithms\25_combinations\lecture.md',
    '26_collections.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks\26_collections\lecture.md',
    '27_itertools.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks\27_itertools\lecture.md',
    '28_functools.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks\28_functools\lecture.md',
    '29_python_internals.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks\29_python_internals\lecture.md',
    '30_profiling.md': r'c:\Users\Pavel\Desktop\yandex_review\backend\tasks\30_profiling\lecture.md'
}

for template, target in mapping.items():
    apply_template(template, target)
