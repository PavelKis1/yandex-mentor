import os

def get_lecture_template(title, content, methods, complexity, pitfalls, questions, resources):
    return f"""# {title}

## 📝 О чем это
{content}

## 🛠 Популярные методы
{methods}

## 💡 Основные концепции
(Добавить детали здесь)

## 💻 Базовый код и примеры
(Добавить примеры кода здесь)

## 🚀 Сложность (Time/Space Complexity)
{complexity}

## 💡 Тонкости и "подводные камни"
{pitfalls}

## ❓ Вопросы на собеседовании
{questions}

## 🔗 Ресурсы для изучения
{resources}
"""

def create_template(filename, title, content, methods, complexity, pitfalls, questions, resources):
    content = get_lecture_template(title, content, methods, complexity, pitfalls, questions, resources)
    with open(f'c:/Users/Pavel/Desktop/yandex_review/scripts/archive/lecture_templates/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)

# Templates for 17-22
create_template('17_bfs.md', '📖 Лекция 17: BFS (Breadth-First Search)', 
                'Алгоритм поиска в ширину (BFS) используется для обхода графов и поиска кратчайшего пути в невзвешенных графах.',
                '- `collections.deque`: использование очереди для BFS.\n- Посещение соседей уровнями.',
                '| Тип | Сложность |\n|---|---|\n| Время | O(V + E) |\n| Память | O(V) |',
                '- Не забудьте `visited` множество.',
                '- Как найти кратчайший путь в графе?',
                '- [Python docs: collections](https://docs.python.org/3/library/collections.html)')

create_template('18_dfs.md', '📖 Лекция 18: DFS (Depth-First Search)', 
                'Поиск в глубину (DFS) — алгоритм обхода графа, углубляющийся максимально далеко по ветке перед возвратом.',
                '- Рекурсивная реализация.\n- Стек (для итеративной реализации).',
                '| Тип | Сложность |\n|---|---|\n| Время | O(V + E) |\n| Память | O(V) |',
                '- Риск переполнения стека при глубокой рекурсии.',
                '- Как обнаружить цикл в графе?',
                '- [Wikipedia: DFS](https://en.wikipedia.org/wiki/Depth-first_search)')

create_template('19_toposort.md', '📖 Лекция 19: Топологическая сортировка',
                'Линейное упорядочивание вершин ориентированного ациклического графа (DAG).',
                '- Алгоритм Кана (Kahn\'s algorithm).\n- DFS-базированная сортировка.',
                '| Тип | Сложность |\n|---|---|\n| Время | O(V + E) |\n| Память | O(V) |',
                '- Работает только на DAG.',
                '- Зачем нужна топологическая сортировка?',
                '- [Wikipedia: Topological Sorting](https://en.wikipedia.org/wiki/Topological_sorting)')

create_template('20_union_find.md', '📖 Лекция 20: Union-Find (DSU)',
                'Структура данных для отслеживания множеств, разделенных на непересекающиеся подмножества.',
                '- `find(x)`: поиск представителя.\n- `union(x, y)`: объединение множеств.',
                '| Тип | Сложность |\n|---|---|\n| Время | O(α(N)) (обратная функция Аккермана) |\n| Память | O(N) |',
                '- Использование сжатия путей (path compression) критично.',
                '- Где применить DSU?',
                '- [Wikipedia: DSU](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)')

create_template('21_trie.md', '📖 Лекция 21: Префиксное дерево (Trie)',
                'Древовидная структура данных для эффективного хранения и поиска строк.',
                '- `insert(word)`: вставка слова.\n- `search(word)`: поиск слова.\n- `startsWith(prefix)`: проверка префикса.',
                '| Тип | Сложность |\n|---|---|\n| Время | O(L) где L - длина слова |\n| Память | O(N*L) |',
                '- Может потреблять много памяти.',
                '- Преимущества перед хэш-таблицей?',
                '- [Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie)')

create_template('22_dijkstra.md', '📖 Лекция 22: Алгоритм Дейкстры',
                'Алгоритм поиска кратчайшего пути от одной вершины ко всем остальным в графе с неотрицательными весами.',
                '- Использование `heapq` (приоритетной очереди).',
                '| Тип | Сложность |\n|---|---|\n| Время | O(E + V log V) |\n| Память | O(V) |',
                '- Не работает с отрицательными весами.',
                '- В чем отличие от BFS?',
                '- [Wikipedia: Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)')
