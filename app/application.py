from fastapi import FastAPI

from app.api.api import api_router
from app.lifespan import lifespan
from app.loguru_logging import configure_logging
from app.orm.sql.session import on_database_shutdown, on_database_startup


def create_fastapi_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        lifespan=lifespan,
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
    )

    app.include_router(api_router)

    app.add_event_handler("startup", on_database_startup)
    app.add_event_handler("shutdown", on_database_shutdown)

    return app
