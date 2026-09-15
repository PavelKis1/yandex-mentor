# 📖 Лекция 61: News Feed (Лента новостей)

## 📝 О чем это
Проектирование высоконагруженной системы ленты новостей.

## 💡 Основные концепции
*   **Push Model**: Обновление ленты подписчиков при публикации поста.
*   **Pull Model**: Запрос постов при открытии ленты.
*   **Гибридный подход**: Комбинация для эффективной работы.

## 💻 Базовый код
```python
# Логика получения ленты (упрощенно)
def get_feed(user_id):
    following = db.get_following(user_id)
    posts = db.get_posts(following)
    return sorted(posts, key=lambda x: x.timestamp, reverse=True)
```

## 🚀 Сложность
Зависит от количества подписок и постов.

## 🔗 Ресурсы
*   [System Design Primer](https://github.com/donnemartin/system-design-primer)

# 📖 Лекция: 61 — News Feed (System Design)

## Обзор темы
Разработка системы ленты новостей (как в VK или Twitter).

## Подробный теоретический минимум
- **Push vs Pull**: Push (fan-out on write) — для пользователей с малым числом фолловеров. Pull (fan-out on load) — для селебрити.
- **Хранение**: База данных для постов, кэш для ленты.
