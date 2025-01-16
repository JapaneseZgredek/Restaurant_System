from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from enum import Enum as PyEnum

# Enum for reservation status
class ReservationStatus(PyEnum):
    placed = "placed"
    canceled = "canceled"

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    hour = Column(String, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)  # Client required

    # Relationships
    client = relationship("Client", back_populates="reservations")
    tables = relationship(
        "Table",
        back_populates="reservation",
        cascade="all, delete-orphan"  # Ensures tables are unlinked if reservation is deleted
    )

# Validation to ensure Reservation has a client and at least one table
def validate_reservation(mapper, connection, target):
    if not target.client_id:
        raise IntegrityError(None, None, "A reservation must be associated with a client.")
    if not target.tables or len(target.tables) < 1:
        raise IntegrityError(None, None, "A reservation must include at least one table.")

# Attach event listener to Reservation
event.listen(Reservation, "before_insert", validate_reservation)
event.listen(Reservation, "before_update", validate_reservation)
