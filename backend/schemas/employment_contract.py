from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Base schema for EmploymentContract
class EmploymentContractBase(BaseModel):
    start_date: date = Field(..., title="Start Date")
    end_date: Optional[date] = Field(None, title="End Date")
    salary: float = Field(..., title="Salary")
    position: str = Field(..., title="Position")
    employee_id: int = Field(..., title="Employee ID")

# Create schema
class EmploymentContractCreate(EmploymentContractBase):
    pass

# Update schema
class EmploymentContractUpdate(BaseModel):
    start_date: Optional[date] = Field(None, title="Start Date")
    end_date: Optional[date] = Field(None, title="End Date")
    salary: Optional[float] = Field(None, title="Salary")
    position: Optional[str] = Field(None, title="Position")
    employee_id: Optional[int] = Field(None, title="Employee ID")

# Read schema
class EmploymentContract(BaseModel):
    id: int
    start_date: date
    end_date: Optional[date]
    salary: float
    position: str
    employee_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class EmploymentContractWithRelations(EmploymentContract):
    restaurant_employee: "RestaurantEmployee"


# Import related schemas
from backend.schemas.restaurant_employee import RestaurantEmployee

EmploymentContractWithRelations.update_forward_refs()
