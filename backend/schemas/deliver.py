from pydantic import BaseModel, Field
from typing import List, Optional

# Base schema for Deliver
class DeliverBase(BaseModel):
    company_name: str = Field(..., title="Company Name")
    person_id: int = Field(..., title="Person ID")

# Create schema
class DeliverCreate(DeliverBase):
    pass

# Update schema
class DeliverUpdate(BaseModel):
    company_name: Optional[str] = Field(None, title="Company Name")
    person_id: Optional[int] = Field(None, title="Person ID")

# Read schema
class Deliver(BaseModel):
    id: int
    company_name: str
    person_id: int

    class Config:
        from_attributes = True

# Detailed schema with related objects
class DeliverWithRelations(Deliver):
    deliveries: List["Delivery"] = []


# Import related schemas
from backend.schemas.delivery import Delivery

DeliverWithRelations.update_forward_refs()
