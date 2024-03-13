from enum import Enum

from sqlmodel import Field, SQLModel


# ------------- User -------------


class UserBase(SQLModel):
    username: str = Field(nullable=False, unique=True, index=True)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(primary_key=True, default=None)


# ------------- Product -------------


class ProductBase(SQLModel):
    name: str = Field(index=True, unique=True)
    price: float = Field(nullable=False)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase, table=True):
    __tablename__ = "products"
    id: int | None = Field(primary_key=True, default=None)


# ------------- Cart -------------
class CartBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class Cart(CartBase, table=True):
    __tablename__ = "carts"
    id: int | None = Field(primary_key=True, default=None)


# ------------- CartItem -------------
class CartItemBase(SQLModel):
    cart_id: int = Field(foreign_key="carts.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field()


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    pass


class CartItem(CartItemBase, table=True):
    __tablename__ = "cart_items"
    id: int | None = Field(primary_key=True, default=None)


# ------------- Order -------------
class OrderStatus(str, Enum):
    accepted = "accepted"
    closed = "closed"


class OrderBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    price: float = Field()
    status: OrderStatus = Field()


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase, table=True):
    __tablename__ = "orders"
    id: int | None = Field(primary_key=True, default=None)


# ------------- OrderItem -------------
class OrderItemBase(SQLModel):
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field()


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItem(OrderItemBase, table=True):
    __tablename__ = "order_items"
    id: int | None = Field(primary_key=True, default=None)
