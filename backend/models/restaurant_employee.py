from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

# Enum for roles
class Role(PyEnum):
    waiter = "waiter"
    cook = "cook"
    manager = "manager"
    driver = "driver"
    owner = "owner"

# Association table for RestaurantEmployee and Order (Many-to-Many)
restaurant_employee_order = Table(
    "restaurant_employee_order",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("restaurant_employee.id", ondelete="CASCADE"), primary_key=True),
    Column("order_id", Integer, ForeignKey("order.id", ondelete="CASCADE"), primary_key=True)
)

class RestaurantEmployee(Base):
    __tablename__ = "restaurant_employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_identificator = Column(String, unique=True, nullable=False)
    role = Column(Enum(Role), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)  # Ensure cascade delete

    # Relationships
    person = relationship("Person", back_populates="restaurant_employee")
    employment_contract = relationship("EmploymentContract", back_populates="restaurant_employee", cascade="all, delete")
    orders = relationship(
        "Order",
        secondary=restaurant_employee_order,
        back_populates="restaurant_employee"
    )

# Validation to ensure a RestaurantEmployee is always linked to a Person
def validate_restaurant_employee_person(mapper, connection, target):
    if not target.person_id:
        raise IntegrityError(None, None, "A RestaurantEmployee must be associated with a Person.")

# Attach event listener to RestaurantEmployee
event.listen(RestaurantEmployee, "before_insert", validate_restaurant_employee_person)
event.listen(RestaurantEmployee, "before_update", validate_restaurant_employee_person)
