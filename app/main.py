from contextlib import asynccontextmanager
from loguru import logger
from app.api.routers.departments import router as departments_router
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Инициализация приложения')
    yield
    logger.info("Завершение приложения")


def create_app() -> FastAPI:
    app = FastAPI(title="API hitalent", description="Сервис API организационной структуры", lifespan=lifespan)
    app.include_router(departments_router)
    return app

app = create_app()