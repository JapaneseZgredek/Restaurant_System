from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.delivery import Delivery as DeliveryModel, delivery_ingredient
from backend.schemas.delivery import DeliveryCreate, DeliveryUpdate, Delivery, DeliveryWithRelations
from backend.models.ingredient import Ingredient as IngredientModel

router = APIRouter(
    prefix="/delivery",
    tags=["Delivery"],
)

# Get all Delivery records
@router.get("/", response_model=list[Delivery])
def get_all_deliveries(db: Session = Depends(get_db)):
    return db.query(DeliveryModel).all()

# Get a specific Delivery record by ID
@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    return delivery

# Create a new Delivery record
@router.post("/", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    ingredient_records = db.query(IngredientModel).filter(IngredientModel.id.in_(delivery.ingredient_ids)).all()
    if len(ingredient_records) != len(delivery.ingredient_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more Ingredient IDs are invalid"
        )
    new_delivery = DeliveryModel(
        status=delivery.status,
        date=delivery.date,
        deliver_id=delivery.deliver_id,
        ingredients=ingredient_records
    )
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery

# Update an existing Delivery record
@router.put("/{delivery_id}", response_model=Delivery)
def update_delivery(delivery_id: int, delivery: DeliveryUpdate, db: Session = Depends(get_db)):
    db_delivery = db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    if delivery.ingredient_ids:
        ingredient_records = db.query(IngredientModel).filter(IngredientModel.id.in_(delivery.ingredient_ids)).all()
        if len(ingredient_records) != len(delivery.ingredient_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more Ingredient IDs are invalid"
            )
        db_delivery.ingredients = ingredient_records
    for key, value in delivery.dict(exclude_unset=True).items():
        if key != "ingredient_ids":
            setattr(db_delivery, key, value)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

# Delete a Delivery record by ID
@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    db.delete(db_delivery)
    db.commit()
    return

# Get a Delivery record with all related objects
@router.get("/{delivery_id}/with-relations", response_model=DeliveryWithRelations)
def get_delivery_with_relations(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    return delivery
