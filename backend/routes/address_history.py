from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.address_history import AddressHistory as AddressHistoryModel
from backend.schemas.address_history import (
    AddressHistory,
    AddressHistoryCreate,
    AddressHistoryUpdate,
    AddressHistoryWithRelations,
)

router = APIRouter(prefix="/address-history", tags=["AddressHistory"])

# Retrieve all records
@router.get("/", response_model=List[AddressHistory])
def get_all_address_histories(db: Session = Depends(get_db)):
    return db.query(AddressHistoryModel).all()

# Retrieve a specific record by ID
@router.get("/{address_history_id}", response_model=AddressHistory)
def get_address_history(address_history_id: int, db: Session = Depends(get_db)):
    address_history = db.query(AddressHistoryModel).filter(AddressHistoryModel.id == address_history_id).first()
    if not address_history:
        raise HTTPException(status_code=404, detail="AddressHistory not found")
    return address_history

# Retrieve a specific record with related objects
@router.get("/{address_history_id}/details", response_model=AddressHistoryWithRelations)
def get_address_history_with_relations(address_history_id: int, db: Session = Depends(get_db)):
    address_history = (
        db.query(AddressHistoryModel)
        .filter(AddressHistoryModel.id == address_history_id)
        .first()
    )
    if not address_history:
        raise HTTPException(status_code=404, detail="AddressHistory not found")
    return address_history

# Create a new record
@router.post("/", response_model=AddressHistory)
def create_address_history(address_history: AddressHistoryCreate, db: Session = Depends(get_db)):
    new_address_history = AddressHistoryModel(**address_history.dict())
    db.add(new_address_history)
    db.commit()
    db.refresh(new_address_history)
    return new_address_history

# Update an existing record
@router.put("/{address_history_id}", response_model=AddressHistory)
def update_address_history(
    address_history_id: int,
    address_history_data: AddressHistoryUpdate,
    db: Session = Depends(get_db),
):
    address_history = db.query(AddressHistoryModel).filter(AddressHistoryModel.id == address_history_id).first()
    if not address_history:
        raise HTTPException(status_code=404, detail="AddressHistory not found")
    for key, value in address_history_data.dict(exclude_unset=True).items():
        setattr(address_history, key, value)
    db.commit()
    db.refresh(address_history)
    return address_history

# Delete a record by ID
@router.delete("/{address_history_id}", status_code=204)
def delete_address_history(address_history_id: int, db: Session = Depends(get_db)):
    address_history = db.query(AddressHistoryModel).filter(AddressHistoryModel.id == address_history_id).first()
    if not address_history:
        raise HTTPException(status_code=404, detail="AddressHistory not found")
    db.delete(address_history)
    db.commit()
    return None
