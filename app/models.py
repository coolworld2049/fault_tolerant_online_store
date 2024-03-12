from enum import Enum

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel
from sqlmodel import SQLModel, Field


class BaseSQLModel(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    model_config = ConfigDict(
        alias_generator=to_camel, arbitrary_types_allowed=True, populate_by_name=True
    )


# ------------- User -------------


class UserBase(BaseSQLModel):
    username: str = Field(nullable=False, unique=True, index=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase, table=True):
    __tablename__ = "users"


class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int | None = None


# ------------- Product -------------


class ProductBase(BaseSQLModel):
    name: str = Field(index=True, unique=True)
    price: float = Field(nullable=False)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase, table=True):
    __tablename__ = "products"


class ProductOut(ProductBase):
    id: int


class ProductsOut(SQLModel):
    data: list[ProductOut]
    count: int | None = None


# ------------- Cart -------------
class CartBase(BaseSQLModel):
    user_id: int = Field(foreign_key="users.id")


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class Cart(CartBase, table=True):
    __tablename__ = "carts"


class CartOut(CartBase):
    id: int


class CartsOut(SQLModel):
    data: list[CartOut]
    count: int | None = None


# ------------- CartItem -------------
class CartItemBase(BaseSQLModel):
    cart_id: int = Field(foreign_key="carts.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field()


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    pass


class CartItem(CartItemBase, table=True):
    __tablename__ = "cart_items"


class CartItemOut(CartItemBase):
    id: int


class CartItemsOut(SQLModel):
    data: list[CartItemOut]
    count: int | None = None


# ------------- Order -------------
class OrderStatus(str, Enum):
    accepted = "accepted"
    closed = "closed"


class OrderBase(BaseSQLModel):
    user_id: int = Field(foreign_key="users.id")
    price: float = Field()
    status: OrderStatus = Field()


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase, table=True):
    __tablename__ = "orders"


class OrderOut(OrderBase):
    id: int


class OrdersOut(SQLModel):
    data: list[OrderOut]
    count: int | None = None


# ------------- Order -------------
class OrderItemBase(BaseSQLModel):
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field()


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"


class OrderItemOut(OrderItemBase):
    id: int


class OrderItemsOut(SQLModel):
    data: list[OrderItemOut]
    count: int | None = None
