from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.client import Client as ClientModel
from backend.schemas.client import (
    Client,
    ClientCreate,
    ClientUpdate,
    ClientWithRelations,
)

router = APIRouter(prefix="/clients", tags=["Clients"])

# Retrieve all clients
@router.get("/", response_model=List[Client])
def get_all_clients(db: Session = Depends(get_db)):
    return db.query(ClientModel).all()

# Retrieve a specific client by ID
@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Retrieve a specific client with related objects
@router.get("/{client_id}/details", response_model=ClientWithRelations)
def get_client_with_relations(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

# Create a new client
@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = ClientModel(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# Update an existing client
@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client_data.dict(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

# Delete a client by ID
@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return None
