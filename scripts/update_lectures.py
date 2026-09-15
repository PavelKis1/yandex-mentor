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

def update_lecture(file_path, new_content):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated: {file_path}")
    except Exception as e:
        print(f"Failed to update {file_path}: {e}")

# Example update for Lecture 01
title_01 = "📖 Лекция 01: Хеш-таблицы (Hash Tables)"
content_01 = "Хеш-таблицы — это фундаментальная структура данных, обеспечивающая среднее время поиска, вставки и удаления O(1). В Python они лежат в основе `dict` и `set`."
methods_01 = """
### Для dict:
- `dict.get(key, default)`: безопасное получение значения.
- `dict.keys()`, `dict.values()`, `dict.items()`: получение ключей, значений или пар.
- `dict.pop(key)`: удаление элемента.
- `dict.update(other)`: обновление словаря.

### Для set:
- `set.add(item)`: добавление элемента.
- `set.remove(item)`: удаление элемента.
- `set.union(other)`, `set.intersection(other)`: объединение и пересечение.
"""
complexity_01 = "| Операция | Среднее | Худшее |\n|---|---|---|\n| Поиск | O(1) | O(n) |\n| Вставка | O(1) | O(n) |\n| Удаление | O(1) | O(n) |"
pitfalls_01 = "- Не используйте изменяемые объекты (например, list) в качестве ключей dict или элементов set.\n- При большом количестве коллизий производительность деградирует до O(n)."
questions_01 = "- Как устроена хеш-таблица в Python?\n- Что такое коллизии и как Python их решает?\n- Почему list нельзя использовать как ключ в dict?"
resources_01 = "- [Python Documentation: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)\n- [MDN: Map Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)"

new_content_01 = get_lecture_template(title_01, content_01, methods_01, complexity_01, pitfalls_01, questions_01, resources_01)
update_lecture('c:/Users/Pavel/Desktop/yandex_review/backend/algorithms/01_hash_tables/lecture.md', new_content_01)
