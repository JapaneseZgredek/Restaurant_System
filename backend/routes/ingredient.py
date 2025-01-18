from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.ingredient import Ingredient as IngredientModel
from backend.schemas.ingredient import (
    IngredientCreate,
    IngredientUpdate,
    Ingredient,
    IngredientWithRelations,
)

router = APIRouter(
    prefix="/ingredient",
    tags=["Ingredient"],
)

# Get all Ingredient records
@router.get("/", response_model=list[Ingredient])
def get_all_ingredients(db: Session = Depends(get_db)):
    return db.query(IngredientModel).all()

# Get a specific Ingredient record by ID
@router.get("/{ingredient_id}", response_model=Ingredient)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient

# Create a new Ingredient record
@router.post("/", response_model=Ingredient, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    new_ingredient = IngredientModel(
        name=ingredient.name,
        amount=ingredient.amount,
        metric=ingredient.metric
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient

# Update an existing Ingredient record
@router.put("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db)):
    db_ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    for key, value in ingredient.dict(exclude_unset=True).items():
        setattr(db_ingredient, key, value)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

# Delete an Ingredient record by ID
@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    db.delete(db_ingredient)
    db.commit()
    return

# Get an Ingredient record with all related objects
@router.get("/{ingredient_id}/with-relations", response_model=IngredientWithRelations)
def get_ingredient_with_relations(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(IngredientModel).filter(IngredientModel.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found")
    return ingredient
