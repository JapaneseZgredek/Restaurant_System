from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.deliver import Deliver as DeliverModel
from backend.schemas.deliver import DeliverCreate, DeliverUpdate, Deliver, DeliverWithRelations

router = APIRouter(
    prefix="/deliver",
    tags=["Deliver"],
)

# Get all Deliver records
@router.get("/", response_model=list[Deliver])
def get_all_delivers(db: Session = Depends(get_db)):
    return db.query(DeliverModel).all()

# Get a specific Deliver record by ID
@router.get("/{deliver_id}", response_model=Deliver)
def get_deliver(deliver_id: int, db: Session = Depends(get_db)):
    deliver = db.query(DeliverModel).filter(DeliverModel.id == deliver_id).first()
    if not deliver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deliver not found")
    return deliver

# Create a new Deliver record
@router.post("/", response_model=Deliver, status_code=status.HTTP_201_CREATED)
def create_deliver(deliver: DeliverCreate, db: Session = Depends(get_db)):
    new_deliver = DeliverModel(**deliver.dict())
    db.add(new_deliver)
    db.commit()
    db.refresh(new_deliver)
    return new_deliver

# Update an existing Deliver record
@router.put("/{deliver_id}", response_model=Deliver)
def update_deliver(deliver_id: int, deliver: DeliverUpdate, db: Session = Depends(get_db)):
    db_deliver = db.query(DeliverModel).filter(DeliverModel.id == deliver_id).first()
    if not db_deliver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deliver not found")
    for key, value in deliver.dict(exclude_unset=True).items():
        setattr(db_deliver, key, value)
    db.commit()
    db.refresh(db_deliver)
    return db_deliver

# Delete a Deliver record by ID
@router.delete("/{deliver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deliver(deliver_id: int, db: Session = Depends(get_db)):
    db_deliver = db.query(DeliverModel).filter(DeliverModel.id == deliver_id).first()
    if not db_deliver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deliver not found")
    db.delete(db_deliver)
    db.commit()
    return

# Get a Deliver record with all related objects
@router.get("/{deliver_id}/with-relations", response_model=DeliverWithRelations)
def get_deliver_with_relations(deliver_id: int, db: Session = Depends(get_db)):
    deliver = db.query(DeliverModel).filter(DeliverModel.id == deliver_id).first()
    if not deliver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deliver not found")
    return deliver
