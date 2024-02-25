from abc import ABC
from typing import Any

from app import schemas
from app.orm.abc import GenericRepository
from app.orm.sql.abc import GenericSqlRepository


class UserReposityBase(GenericRepository[schemas.User], ABC):
    pass


class UserRepository(GenericSqlRepository[schemas.User], UserReposityBase):
    def __init__(self, session: Any) -> None:
        super().__init__(session, schemas.User)
