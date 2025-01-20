from pydantic import BaseModel, Field
from typing import List, Optional

# Base schema for Order
class OrderBase(BaseModel):
    status: str = Field(..., title="Order Status")
    number: str = Field(..., title="Order Number")
    hour: Optional[str] = Field(None, title="Order Hour")
    payment: str = Field(..., title="Payment Type")
    takeaway_or_onsite: str = Field(..., title="Order Type")
    note: Optional[str] = Field(None, title="Note")
    delay: bool = Field(False, title="Delay")
    client_id: int = Field(..., title="Client ID")
    address_history_id: int = Field(..., title="Address History ID")

# Create schema
class OrderCreate(OrderBase):
    dish_ids: List[int] = Field(..., title="Dish IDs")
    restaurant_employee_ids: List[int] = Field(..., title="Restaurant Employee IDs")

# Update schema
class OrderUpdate(BaseModel):
    status: Optional[str] = Field(None, title="Order Status")
    number: Optional[str] = Field(None, title="Order Number")
    hour: Optional[str] = Field(None, title="Order Hour")
    payment: Optional[str] = Field(None, title="Payment Type")
    takeaway_or_onsite: Optional[str] = Field(None, title="Order Type")
    note: Optional[str] = Field(None, title="Note")
    delay: Optional[bool] = Field(None, title="Delay")
    client_id: Optional[int] = Field(None, title="Client ID")
    address_history_id: Optional[int] = Field(None, title="Address History ID")
    dish_ids: Optional[List[int]] = Field(None, title="Dish IDs")
    restaurant_employee_ids: Optional[List[int]] = Field(None, title="Restaurant Employee IDs")

# Read schema
class Order(BaseModel):
    id: int
    status: str
    number: str
    hour: Optional[str]
    payment: str
    takeaway_or_onsite: str
    note: Optional[str]
    delay: bool
    client_id: int
    address_history_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class OrderWithRelations(Order):
    client: "Client"
    address_history: "AddressHistory"
    restaurant_employee: List["RestaurantEmployee"] = []
    dishes: List["Dish"] = []


# Import related schemas to resolve circular references
from backend.schemas.client import Client
from backend.schemas.address_history import AddressHistory
from backend.schemas.restaurant_employee import RestaurantEmployee
from backend.schemas.dish import Dish

OrderWithRelations.update_forward_refs()
