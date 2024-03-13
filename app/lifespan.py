from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed

from app.orm.cassandra.session import create_cassandra_session
from app.orm.redis.session import create_redis_sentinel
from app.orm.sql.session import sql_session_factory
from app.settings import settings


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup")
    try:

        app.state.sql_session_factory = sql_session_factory

        sentinel = create_redis_sentinel(
            sentinel_nodes=settings.REDIS_SENTINEL_NODES,
            master_name=settings.REDIS_MASTER_NAME,
        )
        app.state.redis_sentinel = sentinel

        cassandra_session = create_cassandra_session(
            contact_points=settings.CASSANDRA_NODES,
        )
        app.state.cassandra_session = cassandra_session
    except Exception as e:
        logger.error(e)

    yield
    logger.info("shutdown")
