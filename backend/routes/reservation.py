from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.reservation import Reservation as ReservationModel
from backend.models.table import Table as TableModel
from backend.models.client import Client as ClientModel
from backend.schemas.reservation import (
    ReservationCreate,
    ReservationUpdate,
    Reservation,
    ReservationWithRelations,
)

router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"],
)

# Get all Reservation records
@router.get("/", response_model=list[Reservation])
def get_all_reservations(db: Session = Depends(get_db)):
    return db.query(ReservationModel).all()

# Get a specific Reservation record by ID
@router.get("/{reservation_id}", response_model=Reservation)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation

# Create a new Reservation record
@router.post("/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Validate client existence
    client = db.query(ClientModel).filter(ClientModel.id == reservation.client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid client ID")

    # Validate and fetch tables
    tables = db.query(TableModel).filter(TableModel.id.in_(reservation.table_ids)).all()
    if len(tables) != len(reservation.table_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table IDs")

    if not tables:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A reservation must include at least one table")

    # Create new reservation
    new_reservation = ReservationModel(
        date=reservation.date,
        hour=reservation.hour,
        number_of_people=reservation.number_of_people,
        status=reservation.status,
        client_id=reservation.client_id,
        tables=tables,
    )
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# Update an existing Reservation record
@router.put("/{reservation_id}", response_model=Reservation)
def update_reservation(reservation_id: int, reservation: ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    if reservation.table_ids:
        tables = db.query(TableModel).filter(TableModel.id.in_(reservation.table_ids)).all()
        if len(tables) != len(reservation.table_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table IDs")
        db_reservation.tables = tables

    for key, value in reservation.dict(exclude_unset=True).items():
        if key != "table_ids":
            setattr(db_reservation, key, value)

    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Delete a Reservation record by ID
@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return

# Get a Reservation record with all related objects
@router.get("/{reservation_id}/with-relations", response_model=ReservationWithRelations)
def get_reservation_with_relations(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(ReservationModel).filter(ReservationModel.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation
