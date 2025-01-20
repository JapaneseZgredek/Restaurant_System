from pydantic import BaseModel, Field
from typing import Optional

# Base schema for Person
class PersonBase(BaseModel):
    name: str = Field(..., title="Name")
    surname: str = Field(..., title="Surname")
    email: str = Field(..., title="Email")
    phone_number: str = Field(..., title="Phone Number")

# Create schema
class PersonCreate(PersonBase):
    pass

# Update schema
class PersonUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Name")
    surname: Optional[str] = Field(None, title="Surname")
    email: Optional[str] = Field(None, title="Email")
    phone_number: Optional[str] = Field(None, title="Phone Number")

# Read schema
class Person(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True

# Detailed schema with related objects
class PersonWithRelations(Person):
    restaurant_employee: Optional["RestaurantEmployee"] = None
    client: Optional["Client"] = None
    deliver: Optional["Deliver"] = None


# Import related schemas to resolve circular references
from backend.schemas.restaurant_employee import RestaurantEmployee
from backend.schemas.client import Client
from backend.schemas.deliver import Deliver

PersonWithRelations.update_forward_refs()
