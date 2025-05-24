from typing import Optional

from pydantic import BaseModel, ConfigDict



class CategoryBase(BaseModel):
    name: str

class CategoryRead(CategoryBase):
    model_config=ConfigDict(from_attributes=True)
    id: int

class CategoryCreate(CategoryBase):
    pass 

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
