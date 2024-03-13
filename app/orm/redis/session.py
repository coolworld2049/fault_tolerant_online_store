import redis
from redis import Sentinel


def create_redis_sentinel(
    sentinel_nodes: list[tuple[str, int]], master_name: str
) -> redis.Redis:
    sentinel = Sentinel(sentinel_nodes, socket_timeout=0.1)
    return sentinel
