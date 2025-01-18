from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.order import Order as OrderModel
from backend.models.dish import Dish as DishModel
from backend.models.restaurant_employee import RestaurantEmployee as RestaurantEmployeeModel
from backend.schemas.order import (
    OrderCreate,
    OrderUpdate,
    Order,
    OrderWithRelations,
)

router = APIRouter(
    prefix="/order",
    tags=["Order"],
)

# Get all Order records
@router.get("/", response_model=list[Order])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(OrderModel).all()

# Get a specific Order record by ID
@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

# Create a new Order record
@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Validate and fetch related dishes and employees
    dishes = db.query(DishModel).filter(DishModel.id.in_(order.dish_ids)).all()
    if len(dishes) != len(order.dish_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid dish IDs")

    employees = db.query(RestaurantEmployeeModel).filter(
        RestaurantEmployeeModel.id.in_(order.restaurant_employee_ids)
    ).all()
    if len(employees) != len(order.restaurant_employee_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee IDs")

    if len(employees) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An order must have at least two employees")

    # Create new order
    new_order = OrderModel(
        status=order.status,
        number=order.number,
        hour=order.hour,
        payment=order.payment,
        takeaway_or_onsite=order.takeaway_or_onsite,
        note=order.note,
        delay=order.delay,
        client_id=order.client_id,
        address_history_id=order.address_history_id,
        dishes=dishes,
        restaurant_employee=employees,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Update an existing Order record
@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.dish_ids:
        dishes = db.query(DishModel).filter(DishModel.id.in_(order.dish_ids)).all()
        if len(dishes) != len(order.dish_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid dish IDs")
        db_order.dishes = dishes

    if order.restaurant_employee_ids:
        employees = db.query(RestaurantEmployeeModel).filter(
            RestaurantEmployeeModel.id.in_(order.restaurant_employee_ids)
        ).all()
        if len(employees) != len(order.restaurant_employee_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee IDs")
        if len(employees) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An order must have at least two employees")
        db_order.restaurant_employee = employees

    for key, value in order.dict(exclude_unset=True).items():
        if key not in {"dish_ids", "restaurant_employee_ids"}:
            setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

# Delete an Order record by ID
@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return

# Get an Order record with all related objects
@router.get("/{order_id}/with-relations", response_model=OrderWithRelations)
def get_order_with_relations(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
