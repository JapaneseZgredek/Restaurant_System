from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class DeliveryBase(BaseModel):
    delivery_status: str = Field(..., title="Delivery Status")  # Renamed from `status`
    delivery_date: date = Field(..., title="Delivery Date")     # Renamed from `date`
    deliver_id: int = Field(..., title="Deliver ID")

class DeliveryCreate(DeliveryBase):
    ingredient_ids: List[int] = Field(..., title="Ingredient IDs")

class DeliveryUpdate(BaseModel):
    delivery_status: Optional[str] = Field(None, title="Delivery Status")
    delivery_date: Optional[date] = Field(None, title="Delivery Date")
    deliver_id: Optional[int] = Field(None, title="Deliver ID")
    ingredient_ids: Optional[List[int]] = Field(None, title="Ingredient IDs")

class Delivery(BaseModel):
    id: int
    delivery_status: str
    delivery_date: date
    deliver_id: int

    class Config:
        from_attributes = True

class DeliveryWithRelations(Delivery):
    deliver: "Deliver"
    ingredients: List["Ingredient"] = []


from backend.schemas.deliver import Deliver
from backend.schemas.ingredient import Ingredient

DeliveryWithRelations.update_forward_refs()
