import socket
from collections import deque
from contextlib import closing
from typing import Any

from loguru import logger
from sqlalchemy import NullPool
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session

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


def check_socket(host, port, timeout):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False


class RoutingSession(Session):

    def get_bind(
        self,
        mapper=None,
        clause=None,
        **kwargs: Any,
    ):
        counter = len(engines)
        while counter > 0:
            engine = engines[0]
            engines.rotate(-1)
            counter -= 1
            try:
                if not check_socket(engine.url.host, engine.url.port, 3):
                    raise ConnectionError(engine.url)
                logger.debug(f"Connection to {engine.url} successful.")
                return engine
            except ConnectionError as e:
                logger.warning(f"Connection to {engine.url} failed: {e}")
                continue
        else:
            logger.error("Could not connect to any url")


sql_session_factory = sessionmaker(class_=RoutingSession, autoflush=False)
