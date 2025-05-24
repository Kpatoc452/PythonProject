from pydantic import BaseModel, ConfigDict

class PurchaseRead(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    user_id: int
    product_id: int
    id: int