from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Purchase(Base, IdIntPkMixin):
    __tablename__ = "Purchase"

    product_id: Mapped[int] = mapped_column(ForeignKey('Products.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    buyer: Mapped['User'] = relationship(back_populates='purchases')
    product: Mapped['Product'] = relationship(back_populates='purchase')
