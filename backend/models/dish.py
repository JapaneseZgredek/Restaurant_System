from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

# Association table for Dish and Ingredient (Many-to-Many)
dish_ingredient = Table(
    "dish_ingredient",
    Base.metadata,
    Column("dish_id", Integer, ForeignKey("dish.id", ondelete="CASCADE"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), primary_key=True)
)

class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)

    # Relationships
    orders = relationship(
        "Order",
        secondary="order_dish",
        back_populates="dishes"
    )  # Many-to-many with Order
    ingredients = relationship(
        "Ingredient",
        secondary=dish_ingredient,
        back_populates="dishes",
        cascade="all, delete"  # Composition
    )

# Validation to ensure a dish has at least 2 ingredients
def validate_dish_ingredients(mapper, connection, target):
    if len(target.ingredients) < 2:
        raise IntegrityError(None, None, "A dish must have at least 2 ingredients.")

# Attach event listener to Dish
event.listen(Dish, "before_insert", validate_dish_ingredients)
event.listen(Dish, "before_update", validate_dish_ingredients)
