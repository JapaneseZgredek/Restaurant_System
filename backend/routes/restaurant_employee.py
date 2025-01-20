from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.restaurant_employee import RestaurantEmployee as RestaurantEmployeeModel
from backend.models.person import Person as PersonModel
from backend.models.order import Order as OrderModel
from backend.models.employment_contract import EmploymentContract as EmploymentContractModel
from backend.schemas.restaurant_employee import (
    RestaurantEmployeeCreate,
    RestaurantEmployeeUpdate,
    RestaurantEmployee,
)


router = APIRouter(
    prefix="/restaurant_employee",
    tags=["Restaurant Employee"],
)

# Get all RestaurantEmployee records
@router.get("/", response_model=list[RestaurantEmployee])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(RestaurantEmployeeModel).all()

# Get a specific RestaurantEmployee record by ID
@router.get("/{employee_id}", response_model=RestaurantEmployee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant Employee not found")
    return employee

# Create a new RestaurantEmployee record
@router.post("/", response_model=RestaurantEmployee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: RestaurantEmployeeCreate, db: Session = Depends(get_db)):
    # Validate person existence
    person = db.query(PersonModel).filter(PersonModel.id == employee.person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Person ID")

    # Create new employee
    new_employee = RestaurantEmployeeModel(
        employee_identificator=employee.employee_identificator,
        role=employee.role,
        person_id=employee.person_id,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# Update an existing RestaurantEmployee record
@router.put("/{employee_id}", response_model=RestaurantEmployee)
def update_employee(employee_id: int, employee: RestaurantEmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant Employee not found")

    for key, value in employee.dict(exclude_unset=True).items():
        setattr(db_employee, key, value)

    db.commit()
    db.refresh(db_employee)
    return db_employee

# Delete a RestaurantEmployee record by ID
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant Employee not found")
    db.delete(db_employee)
    db.commit()
    return

# Get a RestaurantEmployee record with all related objects
# Had to do different approach here when getting employee with relations, cause encountered some error with typical approach to get this type of data (example in dish routes)
@router.get("/{employee_id}/with-relations")
def get_employee_with_relations(employee_id: int, db: Session = Depends(get_db)):
    # Get data from RestaurantEmployee table
    employee = db.query(RestaurantEmployeeModel).filter(RestaurantEmployeeModel.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant Employee not found")
    # Get data from based on person id
    person = db.query(PersonModel).filter(PersonModel.id == employee.person_id).first()

    # Get data from employment_contract based on employee id
    employment_contract = db.query(EmploymentContractModel).filter(EmploymentContractModel.employee_id == employee.id).first()

    # Get orders
    orders = db.query(OrderModel).filter(OrderModel.restaurant_employee.any(id=employee.id)).all()

    # Format data to response
    response_data = {
        "id": employee.id,
        "employee_identificator": employee.employee_identificator,
        "role": employee.role.value,
        "person": {
            "id": person.id,
            "name": person.name,
            "surname": person.surname,
            "email": person.email,
            "phone_number": person.phone_number
        } if person else None,
        "employment_contract": {
            "id": employment_contract.id,
            "start_date": employment_contract.start_date,
            "end_date": employment_contract.end_date,
            "salary": employment_contract.salary,
            "position": employment_contract.position.value
        } if employment_contract else None,
        "orders": [
            {
                "id": order.id,
                "status": order.status.value,
                "number": order.number,
                "payment": order.payment.value,
                "note": order.note
            }
            for order in orders
        ] if orders else []
    }

    return response_data

