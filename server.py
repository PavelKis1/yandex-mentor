"""Совместимая точка входа (uvicorn server:app).

Весь код — в пакете src/. Этот файл сохранён, чтобы не менять команды запуска:
  Dockerfile, start_mentor.bat и README продолжают работать без изменений.
"""
from src.main import app


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    from src import config

    uvicorn.run(app, host=config.HOST, port=config.PORT)
