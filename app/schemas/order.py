from sqlmodel import Field

from app.schemas.base import BaseModel


class Order(BaseModel, table=True):
    __tablename__ = "orders"

    user_id: int = Field(foreign_key="users.id")
