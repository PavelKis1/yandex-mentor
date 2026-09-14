"""Сборка FastAPI-приложения + точки запуска.

Запуск сервера: uvicorn server:app --host 0.0.0.0 --port 8000
(server.py — совместимая тонкая обёртка над этим модулем).
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from typing import Optional

from src import config
from src.api.routes import router
from src.core.storage import ensure_storage

security = HTTPBasic(auto_error=False)

def authenticate(request: Request, credentials: Optional[HTTPBasicCredentials] = Depends(security)):
    if request.method == "OPTIONS":
        return None
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    is_correct_username = secrets.compare_digest(
        credentials.username, config.AUTH_USER
    )
    is_correct_password = secrets.compare_digest(
        credentials.password, config.AUTH_PASS
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """При старте: подготовить каталоги данных."""
    ensure_storage()
    yield


def create_app() -> FastAPI:
    """Собрать и сконфигурировать приложение."""
    app = FastAPI(title="Yandex Review API", lifespan=_lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, dependencies=[Depends(authenticate)])
    return app


app = create_app()