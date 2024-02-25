from abc import ABC
from typing import Optional, List, TypeVar

from redis import Sentinel

from app.orm.abc import GenericRepository
from app.schemas.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericRedisRepository(GenericRepository[T], ABC):
    def __init__(self, sentinel: Sentinel, service_name: str, prefix: str) -> None:
        self.master = sentinel.master_for(
            service_name, socket_timeout=0.1, decode_responses=True
        )
        self.slave = sentinel.slave_for(
            service_name, socket_timeout=0.1, decode_responses=True
        )
        self.prefix = prefix

    def _get_key(self, id: int) -> str:
        return f"{self.prefix}:{id}"

    def get_by_id(self, id: int) -> Optional[T]:
        key = self._get_key(id)
        result = self.slave.get(key)
        return T.parse_raw(result) if result else None

    def list(self, **filters) -> List[T]:
        keys = self.slave.keys(f"{self.prefix}:*")
        results = [T.parse_raw(self.slave.get(key)) for key in keys]
        return results

    def add(self, record: T) -> T:
        key = self._get_key(record.id)
        self.master.set(key, record.json())
        return record

    def update(self, record: T) -> T:
        key = self._get_key(record.id)
        if self.slave.exists(key):
            self.master.set(key, record.json())
        return record

    def delete(self, id: int) -> None:
        key = self._get_key(id)
        self.master.delete(key)
