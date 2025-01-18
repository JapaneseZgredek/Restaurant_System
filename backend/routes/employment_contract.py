from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.employment_contract import EmploymentContract as EmploymentContractModel
from backend.models.restaurant_employee import RestaurantEmployee as RestaurantEmployeeModel
from backend.schemas.employment_contract import (
    EmploymentContractCreate,
    EmploymentContractUpdate,
    EmploymentContract,
    EmploymentContractWithRelations,
)

router = APIRouter(
    prefix="/employment_contract",
    tags=["EmploymentContract"],
)

# Get all EmploymentContract records
@router.get("/", response_model=list[EmploymentContract])
def get_all_employment_contracts(db: Session = Depends(get_db)):
    return db.query(EmploymentContractModel).all()

# Get a specific EmploymentContract record by ID
@router.get("/{contract_id}", response_model=EmploymentContract)
def get_employment_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(EmploymentContractModel).filter(EmploymentContractModel.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employment contract not found")
    return contract

# Create a new EmploymentContract record
@router.post("/", response_model=EmploymentContract, status_code=status.HTTP_201_CREATED)
def create_employment_contract(contract: EmploymentContractCreate, db: Session = Depends(get_db)):
    employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == contract.employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Employee ID")
    new_contract = EmploymentContractModel(
        start_date=contract.start_date,
        end_date=contract.end_date,
        salary=contract.salary,
        position=contract.position,
        employee_id=contract.employee_id
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    return new_contract

# Update an existing EmploymentContract record
@router.put("/{contract_id}", response_model=EmploymentContract)
def update_employment_contract(contract_id: int, contract: EmploymentContractUpdate, db: Session = Depends(get_db)):
    db_contract = db.query(EmploymentContractModel).filter(EmploymentContractModel.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employment contract not found")
    if contract.employee_id:
        employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == contract.employee_id).first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Employee ID")
        db_contract.employee_id = contract.employee_id
    for key, value in contract.dict(exclude_unset=True).items():
        setattr(db_contract, key, value)
    db.commit()
    db.refresh(db_contract)
    return db_contract

# Delete an EmploymentContract record by ID
@router.delete("/{contract_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employment_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = db.query(EmploymentContractModel).filter(EmploymentContractModel.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employment contract not found")
    db.delete(db_contract)
    db.commit()
    return

# Get an EmploymentContract record with all related objects
@router.get("/{contract_id}/with-relations", response_model=EmploymentContractWithRelations)
def get_employment_contract_with_relations(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(EmploymentContractModel).filter(EmploymentContractModel.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employment contract not found")
    return contract
