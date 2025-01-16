from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.database import Base
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

class AddressHistory(Base):
    __tablename__ = "address_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    post_code = Column(String, nullable=False)
    building_number = Column(String, nullable=False)
    floor = Column(Integer, nullable=True)
    staircase = Column(String, nullable=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"), nullable=False)  # Client required
    order_id = Column(Integer, ForeignKey("order.id", ondelete="SET NULL"), nullable=True)  # Optional link to Order

    # Relationships
    client = relationship("Client", back_populates="address_history")
    order = relationship("Order", back_populates="address_history")

# Validation to ensure AddressHistory has a client
def validate_address_history_client(mapper, connection, target):
    if not target.client_id:
        raise IntegrityError(None, None, "An address history record must be associated with a client.")

# Attach event listener to AddressHistory
event.listen(AddressHistory, "before_insert", validate_address_history_client)
event.listen(AddressHistory, "before_update", validate_address_history_client)
