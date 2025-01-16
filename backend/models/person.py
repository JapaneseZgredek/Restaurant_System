from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)

    # Relationships with composition
    restaurant_employee = relationship("RestaurantEmployee", back_populates="person", cascade="all, delete")
    client = relationship("Client", back_populates="person", cascade="all, delete")
    deliver = relationship("Deliver", back_populates="person", cascade="all, delete")

# Validation to ensure Person is associated with only one role
def validate_person_roles(mapper, connection, target):
    roles = [
        bool(target.client),
        bool(target.restaurant_employee),
        bool(target.deliver)
    ]
    if sum(roles) > 1:
        raise IntegrityError(None, None, "A person can only be associated with one role (Client, RestaurantEmployee, Deliver).")

# Attach event listener to Person
event.listen(Person, "before_insert", validate_person_roles)
event.listen(Person, "before_update", validate_person_roles)
