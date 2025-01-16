from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_date = Column(DateTime, default=datetime.now, nullable=False)
    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)  # Cascade on delete

    # Relationships
    person = relationship("Person", back_populates="client", cascade="all, delete")
    address_history = relationship(
        "AddressHistory",
        back_populates="client",
        cascade="all, delete"  # Composition
    )
    orders = relationship(
        "Order",
        back_populates="client",
        cascade="all, delete"  # Composition
    )
    reservations = relationship("Reservation", back_populates="client", cascade="all, delete")  # Composition

# Validation to ensure Client has a Person
def validate_client_person(mapper, connection, target):
    if not target.person_id:
        raise IntegrityError(None, None, "A client must be associated with a person.")

# Attach event listener to Client
event.listen(Client, "before_insert", validate_client_person)
event.listen(Client, "before_update", validate_client_person)
