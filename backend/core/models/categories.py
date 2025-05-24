from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .product import Product

class Category(Base, IdIntPkMixin):
    __tablename__ = "Categories"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    products: Mapped[list["Product"]] = relationship(back_populates="category")