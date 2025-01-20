from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from backend.core.database import get_db
from backend.models.dish import Dish as DishModel, dish_ingredient
from backend.models.ingredient import Ingredient as IngredientModel
from backend.schemas.dish import DishCreate, DishUpdate, Dish, DishWithRelations

router = APIRouter(
    prefix="/dish",
    tags=["Dish"],
)

# Get all Dish records
@router.get("/", response_model=list[Dish])
def get_all_dishes(db: Session = Depends(get_db)):
    return db.query(DishModel).all()

# Get a specific Dish record by ID
@router.get("/{dish_id}", response_model=Dish)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    return dish

# Create a new Dish record
@router.post("/", response_model=Dish, status_code=status.HTTP_201_CREATED)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    ingredient_records = db.query(IngredientModel).filter(IngredientModel.id.in_(dish.ingredient_ids)).all()
    if len(ingredient_records) != len(dish.ingredient_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more Ingredient IDs are invalid"
        )
    new_dish = DishModel(
        name=dish.name,
        description=dish.description,
        price=dish.price,
        discount=dish.discount,
        ingredients=ingredient_records
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish

# Update an existing Dish record
@router.put("/{dish_id}", response_model=Dish)
def update_dish(dish_id: int, dish: DishUpdate, db: Session = Depends(get_db)):
    db_dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    if dish.ingredient_ids:
        ingredient_records = db.query(IngredientModel).filter(IngredientModel.id.in_(dish.ingredient_ids)).all()
        if len(ingredient_records) != len(dish.ingredient_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more Ingredient IDs are invalid"
            )
        db_dish.ingredients = ingredient_records
    for key, value in dish.dict(exclude_unset=True).items():
        if key != "ingredient_ids":
            setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return db_dish

# Delete a Dish record by ID
@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    db_dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    db.delete(db_dish)
    db.commit()
    return

# Get a Dish record with all related objects
@router.get("/{dish_id}/with-relations", response_model=DishWithRelations)
def get_dish_with_relations(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(DishModel).filter(DishModel.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dish not found")
    return dish

# Get all Dish records with related object, especially ingredients (used to display in Menu)
@router.get("/dishes/all-with-relations", response_model=List[DishWithRelations])
def get_all_dish_with_relations(db: Session = Depends(get_db)):
    dishes = db.query(DishModel).options(joinedload(DishModel.ingredients)).all()
    if not dishes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No dishes found")
    return dishes
