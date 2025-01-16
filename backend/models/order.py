from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

# Enums for status, payment, and order type
class OrderStatus(PyEnum):
    placed = "placed"
    new = "new"
    ready = "ready"
    paid = "paid"
    to_be_paid = "to_be_paid"
    during_delivery = "during_delivery"
    completed = "completed"

class PaymentType(PyEnum):
    cash = "cash"
    card = "card"
    online = "online"

class OrderType(PyEnum):
    takeaway = "takeaway"
    onsite = "onsite"

# Association table for Order and Dish (Many-to-Many)
order_dish = Table(
    "order_dish",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("order.id", ondelete="CASCADE"), primary_key=True),
    Column("dish_id", Integer, ForeignKey("dish.id", ondelete="CASCADE"), primary_key=True)
)

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(OrderStatus), nullable=False)
    number = Column(String, unique=True, nullable=False)
    hour = Column(String, nullable=True)
    payment = Column(Enum(PaymentType), nullable=False)
    takeaway_or_onsite = Column(Enum(OrderType), nullable=False)
    note = Column(String, nullable=True)
    delay = Column(Boolean, default=False)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)  # Cascade on delete
    address_history_id = Column(Integer, ForeignKey("address_history.id", ondelete="SET NULL"), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="orders")
    address_history = relationship("AddressHistory", back_populates="order")
    restaurant_employee = relationship(
        "RestaurantEmployee",
        secondary="restaurant_employee_order",
        back_populates="orders"
    )
    dishes = relationship("Dish", secondary=order_dish, back_populates="orders")  # Many-to-many with Dish

# Validation to ensure Order has a client, at least one dish, and at least two restaurant employees
def validate_order(mapper, connection, target):
    if not target.client_id:
        raise IntegrityError(None, None, "An order must be associated with a client.")
    if not target.dishes or len(target.dishes) < 1:
        raise IntegrityError(None, None, "An order must include at least one dish.")
    if not target.restaurant_employee or len(target.restaurant_employee) < 2:
        raise IntegrityError(None, None, "An order must be associated with at least two restaurant employees.")

# Attach event listener to Order
event.listen(Order, "before_insert", validate_order)
event.listen(Order, "before_update", validate_order)
