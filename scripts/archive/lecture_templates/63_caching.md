# 📖 Лекция 63: Caching (Кеширование)

## 📝 О чем это
Использование кэша для снижения нагрузки на БД.

## 💡 Основные концепции
*   **Стратегии**: Write-through, Write-back, Cache-aside.
*   **Вытеснение**: LRU, LFU.

## 💻 Базовый код
```python
# LRU Cache decorator
from functools import lru_cache

@lru_cache(maxsize=100)
def get_user(user_id):
    return db.query(user_id)
```

## 🚀 Сложность
$O(1)$ для поиска в кэше.

## 🔗 Ресурсы
*   [Redis Documentation](https://redis.io/documentation)
