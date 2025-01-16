from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Date, Table
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

# Enum for delivery status
class DeliveryStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# Association table for Delivery and Ingredient (Many-to-Many)
delivery_ingredient = Table(
    "delivery_ingredient",
    Base.metadata,
    Column("delivery_id", Integer, ForeignKey("delivery.id", ondelete="CASCADE"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), primary_key=True)
)

class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(DeliveryStatus), nullable=False)
    date = Column(Date, nullable=False)
    deliver_id = Column(Integer, ForeignKey("deliver.id", ondelete="CASCADE"), nullable=False)  # Ensures delivery must have a deliverer

    # Relationships
    deliver = relationship("Deliver", back_populates="deliveries")
    ingredients = relationship(
        "Ingredient",
        secondary=delivery_ingredient,
        back_populates="deliveries"
    )

# Validation to ensure a delivery has a deliverer
def validate_delivery_deliverer(mapper, connection, target):
    if not target.deliver_id:
        raise IntegrityError(None, None, "A delivery must have a deliverer assigned.")

# Validation to ensure a delivery has at least one ingredient
def validate_delivery_ingredients(mapper, connection, target):
    if not target.ingredients or len(target.ingredients) < 1:
        raise IntegrityError(None, None, "A delivery must include at least one ingredient.")

# Attach event listeners to Delivery
event.listen(Delivery, "before_insert", validate_delivery_deliverer)
event.listen(Delivery, "before_update", validate_delivery_deliverer)
event.listen(Delivery, "before_insert", validate_delivery_ingredients)
event.listen(Delivery, "before_update", validate_delivery_ingredients)
