from typing import List, Optional

import redis
from redis.connection import ConnectionPool


def create_redis_session(
    startup_nodes: List[dict], password: Optional[str] = None
) -> redis.Redis:
    connection_pool = ConnectionPool.from_url(
        f"redis://{','.join([node['host'] + ':' + node['port'] for node in startup_nodes])}",
        password=password,
        decode_responses=True,
    )
    return redis.Redis(connection_pool=connection_pool, decode_responses=True)
