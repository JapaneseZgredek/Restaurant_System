from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from enum import Enum as PyEnum

# Enum for measurement units
class Metric(PyEnum):
    grams = "grams"
    milliliters = "milliliters"

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    metric = Column(Enum(Metric), nullable=False)

    # Relationships
    dishes = relationship(
        "Dish",
        secondary="dish_ingredient",
        back_populates="ingredients",
        cascade="all, delete"  # Ensures cascading deletes for composition
    )
    deliveries = relationship(
        "Delivery",
        secondary="delivery_ingredient",
        back_populates="ingredients"
    )
