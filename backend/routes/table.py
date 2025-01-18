from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.table import Table as TableModel
from backend.models.reservation import Reservation as ReservationModel
from backend.schemas.table import (
    TableCreate,
    TableUpdate,
    Table,
    TableWithRelations,
)

router = APIRouter(
    prefix="/table",
    tags=["Table"],
)

# Get all Table records
@router.get("/", response_model=list[Table])
def get_all_tables(db: Session = Depends(get_db)):
    return db.query(TableModel).all()

# Get a specific Table record by ID
@router.get("/{table_id}", response_model=Table)
def get_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    return table

# Create a new Table record
@router.post("/", response_model=Table, status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    # Validate reservation existence if reservation_id is provided
    if table.reservation_id:
        reservation = db.query(ReservationModel).filter(ReservationModel.id == table.reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Reservation ID")

    # Create new table
    new_table = TableModel(
        number=table.number,
        number_of_seats=table.number_of_seats,
        reservation_id=table.reservation_id,
    )
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table

# Update an existing Table record
@router.put("/{table_id}", response_model=Table)
def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
    db_table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")

    # Validate reservation existence if reservation_id is updated
    if table.reservation_id:
        reservation = db.query(ReservationModel).filter(ReservationModel.id == table.reservation_id).first()
        if not reservation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Reservation ID")

    for key, value in table.dict(exclude_unset=True).items():
        setattr(db_table, key, value)

    db.commit()
    db.refresh(db_table)
    return db_table

# Delete a Table record by ID
@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    db_table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    db.delete(db_table)
    db.commit()
    return

# Get a Table record with all related objects
@router.get("/{table_id}/with-relations", response_model=TableWithRelations)
def get_table_with_relations(table_id: int, db: Session = Depends(get_db)):
    table = db.query(TableModel).filter(TableModel.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    return table
