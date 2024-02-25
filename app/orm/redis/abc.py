import typing
from abc import ABC
from typing import Optional, List, TypeVar
from redis.asyncio import StrictRedis
from app.orm.abc import GenericRepository
from app.schemas.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericRedisRepository(GenericRepository[T], ABC):
    def __init__(self, host: str, port: int, db: int, prefix: str) -> None:
        self.redis_conn = StrictRedis(host=host, port=port, db=db)
        self.prefix = prefix

    def _get_key(self, id: int) -> str:
        return f"{self.prefix}:{id}"

    def get_by_id(self, id: int) -> Optional[T]:
        key = self._get_key(id)
        result = self.redis_conn.get(key)
        return T.parse_raw(result) if result else None

    def list(self, **filters) -> List[T]:
        # For simplicity, assuming you are storing items as JSON strings in Redis
        keys = self.redis_conn.keys(f"{self.prefix}:*")
        results = [T.parse_raw(self.redis_conn.get(key)) for key in keys]
        return results

    def add(self, record: T) -> T:
        key = self._get_key(record.id)
        self.redis_conn.set(key, record.json())
        return record

    def update(self, record: T) -> T:
        key = self._get_key(record.id)
        if self.redis_conn.exists(key):
            self.redis_conn.set(key, record.json())
        return record

    def delete(self, id: int) -> None:
        key = self._get_key(id)
        self.redis_conn.delete(key)
