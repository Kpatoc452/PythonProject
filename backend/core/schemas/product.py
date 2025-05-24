from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    category_id: int

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image: str
    seller_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sold: Optional[bool] = None
    price: Optional[int] = None
    category_id: Optional[int] = None
