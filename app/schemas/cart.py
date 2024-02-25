from sqlmodel import Field

from app.schemas.base import BaseModel


class Cart(BaseModel, table=True):
    __tablename__ = "carts"

    order_id = Field(foreign_key="users.id")
    product_id = Field(foreign_key="products.id")
    quantity = Field()
