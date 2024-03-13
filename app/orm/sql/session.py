from collections import deque
from typing import Any

from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, SQLModel

from app.settings import settings

engines = deque([create_engine(url) for url in settings.PGPOOL_URLS])
for engine in engines:
    SQLModel.metadata.create_all(engine)


class RoutingSession(Session):
    def get_bind(
        self,
        mapper=None,
        clause=None,
        **kwargs: Any,
    ):
        engine = engines[0]
        engines.rotate(-1)
        logger.debug(f"current engine is a {engine.url}")
        return engine


sql_session_factory = sessionmaker(
    class_=RoutingSession,
    autocommit=False,
    autoflush=False,
)
