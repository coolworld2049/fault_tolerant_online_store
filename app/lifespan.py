from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlmodel import SQLModel

from app.orm.sql.session import create_sqlmodel_engine, create_sqlmodel_session_maker
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    engine = create_sqlmodel_engine(url=settings.DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    session_maker = create_sqlmodel_session_maker(engine)
    app.state.sql_session_factory = session_maker
    yield
    logger.info("shutdown: triggered")
