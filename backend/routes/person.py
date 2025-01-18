from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.person import Person as PersonModel
from backend.schemas.person import (
    PersonCreate,
    PersonUpdate,
    Person,
    PersonWithRelations,
)

router = APIRouter(
    prefix="/person",
    tags=["Person"],
)

# Get all Person records
@router.get("/", response_model=list[Person])
def get_all_people(db: Session = Depends(get_db)):
    persons = db.query(PersonModel).all()
    return persons

# Get a specific Person record by ID
@router.get("/{person_id}", response_model=Person)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person

# Create a new Person record
@router.post("/", response_model=Person, status_code=status.HTTP_201_CREATED)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    new_person = PersonModel(
        name=person.name,
        surname=person.surname,
        email=person.email,
        phone_number=person.phone_number,
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

# Update an existing Person record
@router.put("/{person_id}", response_model=Person)
def update_person(person_id: int, person: PersonUpdate, db: Session = Depends(get_db)):
    db_person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    for key, value in person.dict(exclude_unset=True).items():
        setattr(db_person, key, value)

    db.commit()
    db.refresh(db_person)
    return db_person

# Delete a Person record by ID
@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not db_person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    db.delete(db_person)
    db.commit()
    return

# Get a Person record with all related objects
@router.get("/{person_id}/with-relations", response_model=PersonWithRelations)
def get_person_with_relations(person_id: int, db: Session = Depends(get_db)):
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person
