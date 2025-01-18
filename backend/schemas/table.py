from pydantic import BaseModel, Field
from typing import Optional

# Base schema for Table
class TableBase(BaseModel):
    number: str = Field(..., title="Table Number")
    number_of_seats: int = Field(..., title="Number of Seats")
    reservation_id: Optional[int] = Field(None, title="Reservation ID")

# Create schema
class TableCreate(TableBase):
    pass

# Update schema
class TableUpdate(BaseModel):
    number: Optional[str] = Field(None, title="Table Number")
    number_of_seats: Optional[int] = Field(None, title="Number of Seats")
    reservation_id: Optional[int] = Field(None, title="Reservation ID")

# Read schema
class Table(BaseModel):
    id: int
    number: str
    number_of_seats: int
    reservation_id: Optional[int]

    class Config:
        from_attributes = True

# Detailed schema with related objects
class TableWithRelations(Table):
    reservation: Optional["Reservation"] = None


# Import related schemas
from backend.schemas.reservation import Reservation

TableWithRelations.update_forward_refs()
