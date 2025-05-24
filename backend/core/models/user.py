from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .product import Product
    from .purchase import Purchase
    from .product_views import ProductViews
class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "Users"
    
    
    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)
    
    products: Mapped[list["Product"]] = relationship(back_populates="seller")
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="buyer")
    views: Mapped[list["ProductViews"]] = relationship(back_populates="user")
