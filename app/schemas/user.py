from sqlmodel import Field

from app.schemas.base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    username: str = Field(nullable=False, unique=True, index=True)
