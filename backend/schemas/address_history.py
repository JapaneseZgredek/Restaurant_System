from pydantic import BaseModel, Field
from typing import Optional

# Base schema for AddressHistory
class AddressHistoryBase(BaseModel):
    street: str = Field(..., title="Street", max_length=255)
    city: str = Field(..., title="City", max_length=255)
    post_code: str = Field(..., title="Postal Code", max_length=20)
    building_number: str = Field(..., title="Building Number", max_length=50)
    floor: Optional[int] = Field(None, title="Floor")
    staircase: Optional[str] = Field(None, title="Staircase")
    client_id: int = Field(..., title="Client ID")  # Client is required

# Schema for creating a new AddressHistory
class AddressHistoryCreate(AddressHistoryBase):
    pass  # Same fields as the base schema

# Schema for updating an existing AddressHistory
class AddressHistoryUpdate(BaseModel):
    street: Optional[str] = Field(None, title="Street", max_length=255)
    city: Optional[str] = Field(None, title="City", max_length=255)
    post_code: Optional[str] = Field(None, title="Postal Code", max_length=20)
    building_number: Optional[str] = Field(None, title="Building Number", max_length=50)
    floor: Optional[int] = Field(None, title="Floor")
    staircase: Optional[str] = Field(None, title="Staircase")
    client_id: Optional[int] = Field(None, title="Client ID")
    order_id: Optional[int] = Field(None, title="Order ID")

# Schema for retrieving a single AddressHistory record
class AddressHistory(BaseModel):
    id: int
    street: str
    city: str
    post_code: str
    building_number: str
    floor: Optional[int]
    staircase: Optional[str]
    client_id: int
    order_id: Optional[int]

    class Config:
        from_attributes = True

# Schema for retrieving AddressHistory with related objects
class AddressHistoryWithRelations(AddressHistory):
    client: Optional["Client"] = None
    order: Optional["Order"] = None


# Import-related schemas to resolve circular imports
from backend.schemas.client import Client
from backend.schemas.order import Order

AddressHistoryWithRelations.update_forward_refs()
