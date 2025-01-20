from sqlalchemy import Column, Integer, ForeignKey, Date, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

class Position(PyEnum):
    waiter = "waiter"
    cook = "cook"
    manager = "manager"
    driver = "driver"

class EmploymentContract(Base):
    __tablename__ = "employment_contract"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, default=datetime.now, nullable=False)
    end_date = Column(Date, nullable=True)
    salary = Column(Float, nullable=False)
    position = Column(Enum(Position), nullable=False)
    employee_id = Column(Integer, ForeignKey("restaurant_employee.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    restaurant_employee = relationship("RestaurantEmployee", back_populates="employment_contract")

# Validation to ensure an EmploymentContract is always linked to a RestaurantEmployee
def validate_employment_contract_employee(mapper, connection, target):
    if not target.employee_id:
        raise IntegrityError(None, None, "An EmploymentContract must be associated with a RestaurantEmployee.")

# Attach event listener to EmploymentContract
event.listen(EmploymentContract, "before_insert", validate_employment_contract_employee)
event.listen(EmploymentContract, "before_update", validate_employment_contract_employee)
