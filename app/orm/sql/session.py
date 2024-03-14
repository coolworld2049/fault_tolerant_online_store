import time
from collections import deque
from typing import Any

from loguru import logger
from sqlalchemy import event, Connection, text
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session, SQLModel

from app.settings import settings

engines = deque([create_engine(url, echo=False) for url in settings.PGPOOL_URLS])
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

        def test_conn(_engine):
            try:
                s = _engine.connect()
                s.execute(text("SELECT 1"))
                s.close()
            except ConnectionError as ce:
                logger.debug(ce)
                return False
            else:
                return True

        try:
            test_conn(engine)
        except Exception as e:
            logger.error(e)
            try:
                test_conn(next(engine))
            except StopIteration as se:
                logger.error(se)
        return engine

    _name = None

    def using_bind(self, name):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s


sql_session_factory = sessionmaker(
    class_=RoutingSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=True,
)


def before_cursor_execute(
    conn: Connection, cursor, statement, parameters, context, executemany
):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.debug(f"[{conn.engine.url}] Start Query:\n{statement}")


def after_cursor_execute(
    conn: Connection, cursor, statement, parameters, context, executemany
):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.debug(f"[{conn.engine.url}] Query Complete. Total Time: %f" % total)


for engine in engines:
    event.listen(
        engine,
        "before_cursor_execute",
        before_cursor_execute,
    )
    event.listen(
        engine,
        "after_cursor_execute",
        after_cursor_execute,
    )
