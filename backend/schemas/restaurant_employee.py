from pydantic import BaseModel, Field
from typing import List, Optional

# Base schema for RestaurantEmployee
class RestaurantEmployeeBase(BaseModel):
    employee_identificator: str = Field(..., title="Employee Identificator")
    role: str = Field(..., title="Role")
    person_id: int = Field(..., title="Person ID")

# Create schema
class RestaurantEmployeeCreate(RestaurantEmployeeBase):
    pass

# Update schema
class RestaurantEmployeeUpdate(BaseModel):
    employee_identificator: Optional[str] = Field(None, title="Employee Identificator")
    role: Optional[str] = Field(None, title="Role")
    person_id: Optional[int] = Field(None, title="Person ID")

# Read schema
class RestaurantEmployee(BaseModel):
    id: int
    employee_identificator: str
    role: str
    person_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class RestaurantEmployeeWithRelations(RestaurantEmployee):
    person: "Person"
    employment_contract: Optional["EmploymentContract"] = None
    orders: List["Order"] = []


# Import related schemas
from backend.schemas.person import Person
from backend.schemas.employment_contract import EmploymentContract
from backend.schemas.order import Order

RestaurantEmployeeWithRelations.update_forward_refs()
