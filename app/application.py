import logging
import sys

from fastapi import FastAPI
from loguru import logger

from app.api.api import api_router
from app.lifespan import lifespan
from app.settings import settings


def create_fastapi_app() -> FastAPI:
    logger.add(sys.stdout, level=settings.LOG_LEVEL)
    app = FastAPI(
        lifespan=lifespan,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
    )

    app.include_router(api_router)

    return app
