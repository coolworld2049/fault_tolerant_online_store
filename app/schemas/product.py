from sqlmodel import Field

from app.schemas.base import BaseModel


class Product(BaseModel, table=True):
    __tablename__ = "products"

    name: str = Field(index=True, unique=True)
    price: float = Field(nullable=False)
