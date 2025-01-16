from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

class Deliver(Base):
    __tablename__ = "deliver"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String, unique=True, nullable=False)
    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)  # Composition

    # Relationships
    person = relationship("Person", back_populates="deliver")
    deliveries = relationship("Delivery", back_populates="deliver")  # Cascade delete for linked deliveries

# Validation to ensure Deliver has a Person
def validate_deliver_person(mapper, connection, target):
    if not target.person_id:
        raise IntegrityError(None, None, "A deliver must be associated with a person.")

# Attach event listener to Deliver
event.listen(Deliver, "before_insert", validate_deliver_person)
event.listen(Deliver, "before_update", validate_deliver_person)
