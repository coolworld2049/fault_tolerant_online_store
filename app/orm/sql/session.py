from collections import deque
from typing import Any

from loguru import logger
from sqlalchemy import NullPool
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, SQLModel

from app.settings import settings

engines = deque(
    [
        create_engine(
            url,
            echo=settings.SQLALCHEMY_ECHO,
            future=True,
            poolclass=NullPool,
            pool_pre_ping=True,
        )
        for url in settings.PGPOOL_URLS
    ]
)


def on_database_startup():
    for engine in engines:
        SQLModel.metadata.create_all(engine)


def on_database_shutdown():
    for engine in engines:
        engine.dispose()


class RoutingSession(Session):
    counter = len(engines)

    def get_bind(
        self,
        mapper=None,
        clause=None,
        **kwargs: Any,
    ):
        engine = engines[0]
        engines.rotate(-1)
        logger.debug(f"[{engine.url}]")
        return engine


sql_session_factory = sessionmaker(class_=RoutingSession, autoflush=False)
