# Задания: Fastapi

## Задание 1: Модель Pydantic
Опишите Pydantic-модель Order с полями id, total, items (список) и валидацией total ≥ 0.

**Пример:** `class Order(BaseModel): total: float = Field(ge=0)`

💡 **Подсказка:** BaseModel + Field(ge=0).

## Задание 2: Эндпоинт с валидацией
Создайте GET /healthz и POST /tasks, где тело — модель Task(title: str, done: bool=False).

**Пример:** `app = FastAPI(); @app.post('/tasks')`

💡 **Подсказка:** FastAPI сам возвращает 422 при невалидном теле.

## Задание 3: Зависимости
Создайте зависимость get_db(), которая открывает соединение и закрывает его. Примените к эндпоинту.

**Пример:** `@app.get('/users')
def get_users(db: Session = Depends(get_db))`

💡 **Подсказка:** Depends + yield/генератор в зависимости.
