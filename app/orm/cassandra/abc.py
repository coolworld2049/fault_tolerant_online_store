from abc import ABC
from typing import Optional, List, TypeVar

from cassandra.cluster import Session

from app.orm.abc import GenericRepository
from app.schemas.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericCassandraRepository(GenericRepository[T], ABC):
    def __init__(self, session: Session, table: str) -> None:
        self.session = session
        self.table = table

    def get_by_id(self, id: int) -> Optional[T]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self.session.execute(query, [id])
        return result.one()

    def list(self, **filters) -> List[T]:
        where_clauses = [f"{column} = %s" for column in filters.keys()]
        query = f"SELECT * FROM {self.table}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        result = self.session.execute(query, list(filters.values()))
        return list(result)

    def add(self, record: T) -> T:
        columns = ", ".join(record.__annotations__.keys())
        values = ", ".join(["%s" for _ in record.__annotations__.keys()])
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
        self.session.execute(query, list(record.dict().values()))
        return record

    def update(self, record: T) -> T:
        set_clauses = [f"{column} = %s" for column in record.__annotations__.keys()]
        query = f"UPDATE {self.table} SET {', '.join(set_clauses)} WHERE id = %s"
        values = list(record.dict().values()) + [record.id]
        self.session.execute(query, values)
        return record

    def delete(self, id: int) -> None:
        query = f"DELETE FROM {self.table} WHERE id = %s"
        self.session.execute(query, [id])
