# Задания: Sqlalchemy

## Задание 1: Модель
Опишите модель User(id, name, email unique) на SQLAlchemy (declarative).

**Пример:** `class User(Base): __tablename__='users'; email = Column(String, unique=True)`

💡 **Подсказка:** Declarative Base + Column.

## Задание 2: Запросы
Напишите: получить пользователя по email, всех старше 30, первого отсортированного по id.

**Пример:** `User.query.filter_by(email=e).first()`

💡 **Подсказка:** filter_by для равенства, order_by/limit.

## Задание 3: Связь один-ко-многим
Модели User и Post: один пользователь — много постов. Опишите relationship.

**Пример:** `posts = relationship('Post', back_populates='user')`

💡 **Подсказка:** ForeignKey + relationship.
