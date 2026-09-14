# Задания: Type Hints

## Задание 1: Аннотации коллекций
Аннотируйте функцию group_by_first_letter(words: list[str]) → dict[str, list[str]], группирующую слова по первой букве. Включите Optional и Union где уместно.

**Пример:** `Аннотации проходят mypy без ошибок`

💡 **Подсказка:** from __future__ import annotations; dict[str, list[str]], Optional[str].

## Задание 2: TypedDict для API
Опишите TypedDict UserResponse с полями id: int, name: str, friends: list[int] и функцию, принимающую объект и возвращающую его имя. Проверьте корректность через mypy.

**Пример:** `mypy не ругается на валидный объект и ругается на невалидный`

💡 **Подсказка:** from typing import TypedDict, NotRequired.

## Задание 3: Generics
Напишите обобщённую функцию first(items: Sequence[T]) → T, возвращающую первый элемент, с TypeVar.

**Пример:** `first([1,2]) → 1; first(('a','b')) → 'a'`

💡 **Подсказка:** T = TypeVar('T'); def first(items: Sequence[T]) → T.
