from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, unique=True, nullable=False)
    number_of_seats = Column(Integer, nullable=False)
    reservation_id = Column(Integer, ForeignKey("reservation.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    reservation = relationship("Reservation", back_populates="tables")
