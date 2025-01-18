from pydantic import BaseModel, Field
from typing import List, Optional

# Base schema for Dish
class DishBase(BaseModel):
    name: str = Field(..., title="Dish Name")
    description: Optional[str] = Field(None, title="Dish Description")
    price: float = Field(..., title="Price")
    discount: Optional[float] = Field(None, title="Discount")

# Create schema
class DishCreate(DishBase):
    ingredient_ids: List[int] = Field(..., title="Ingredient IDs")

# Update schema
class DishUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Dish Name")
    description: Optional[str] = Field(None, title="Dish Description")
    price: Optional[float] = Field(None, title="Price")
    discount: Optional[float] = Field(None, title="Discount")
    ingredient_ids: Optional[List[int]] = Field(None, title="Ingredient IDs")

# Read schema
class Dish(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    discount: Optional[float]

    class Config:
        from_attributes = True

# Detailed schema with related objects
class DishWithRelations(Dish):
    ingredients: List["Ingredient"] = []


# Import related schemas
from backend.schemas.ingredient import Ingredient

DishWithRelations.update_forward_refs()
