from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .categories import Category
    from .user import User
    from .purchase import Purchase
    from .product_views import ProductViews

class Product(Base, IdIntPkMixin):
    __tablename__ = "Products"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    image: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    sold: Mapped[bool] = mapped_column(Boolean, default=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("Categories.id"))
    seller: Mapped["User"] = relationship(back_populates="products")
    category: Mapped["Category"] = relationship(back_populates="products")
    purchase: Mapped["Purchase"] = relationship(back_populates="product")
    views: Mapped[list["ProductViews"]] = relationship(back_populates="product")