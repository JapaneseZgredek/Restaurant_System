from pydantic import BaseModel, Field
from typing import List, Optional

# Base schema for Ingredient
class IngredientBase(BaseModel):
    name: str = Field(..., title="Name")
    amount: int = Field(..., title="Amount")
    metric: str = Field(..., title="Measurement Unit")

# Create schema
class IngredientCreate(IngredientBase):
    pass

# Update schema
class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Name")
    amount: Optional[int] = Field(None, title="Amount")
    metric: Optional[str] = Field(None, title="Measurement Unit")

# Read schema
class Ingredient(BaseModel):
    id: int
    name: str
    amount: int
    metric: str

    class Config:
        from_attributes = True

# Detailed schema with related objects
class IngredientWithRelations(Ingredient):
    dishes: List["Dish"] = []
    deliveries: List["Delivery"] = []


# Import related schemas
from backend.schemas.dish import Dish
from backend.schemas.delivery import Delivery

IngredientWithRelations.update_forward_refs()
