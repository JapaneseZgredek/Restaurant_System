from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Base schema for Client
class ClientBase(BaseModel):
    registration_date: datetime = Field(..., title="Registration Date")
    person_id: int = Field(..., title="Person ID")

# Create schema
class ClientCreate(ClientBase):
    pass

# Update schema
class ClientUpdate(BaseModel):
    registration_date: Optional[datetime] = Field(None, title="Registration Date")
    person_id: Optional[int] = Field(None, title="Person ID")

# Read schema
class Client(BaseModel):
    id: int
    registration_date: datetime
    person_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class ClientWithRelations(Client):
    address_history: List["AddressHistory"] = []
    orders: List["Order"] = []
    reservations: List["Reservation"] = []


# Import related schemas to resolve circular references
from backend.schemas.address_history import AddressHistory
from backend.schemas.order import Order
from backend.schemas.reservation import Reservation

ClientWithRelations.update_forward_refs()
