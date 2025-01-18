from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Base schema for Reservation
class ReservationBase(BaseModel):
    reservation_date: date = Field(..., title="Reservation Date")  # Renamed from `date`
    reservation_hour: str = Field(..., title="Reservation Hour")   # Renamed from `hour`
    number_of_people: int = Field(..., title="Number of People")
    status: str = Field(..., title="Reservation Status")
    client_id: int = Field(..., title="Client ID")

# Create schema
class ReservationCreate(ReservationBase):
    table_ids: List[int] = Field(..., title="Table IDs")

# Update schema
class ReservationUpdate(BaseModel):
    reservation_date: Optional[date] = Field(None, title="Reservation Date")
    reservation_hour: Optional[str] = Field(None, title="Reservation Hour")
    number_of_people: Optional[int] = Field(None, title="Number of People")
    status: Optional[str] = Field(None, title="Reservation Status")
    client_id: Optional[int] = Field(None, title="Client ID")
    table_ids: Optional[List[int]] = Field(None, title="Table IDs")

# Read schema
class Reservation(BaseModel):
    id: int
    reservation_date: date  # Renamed from `date`
    reservation_hour: str   # Renamed from `hour`
    number_of_people: int
    status: str
    client_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class ReservationWithRelations(Reservation):
    client: "Client"
    tables: List["Table"] = []

# Import related schemas
from backend.schemas.client import Client
from backend.schemas.table import Table

ReservationWithRelations.update_forward_refs()
