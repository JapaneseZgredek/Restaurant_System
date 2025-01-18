from fastapi import FastAPI
from backend.core.database import initialize_database
from backend.routes.address_history import router as address_history_router
from backend.routes.client import router as client_router
from backend.routes.deliver import router as deliver_router
from backend.routes.delivery import router as delivery_router
from backend.routes.dish import router as dish_router
from backend.routes.employment_contract import router as employment_contract_router
from backend.routes.ingredient import router as ingredient_router
from backend.routes.order import router as order_router
from backend.routes.person import router as person_router
from backend.routes.reservation import router as reservation_router
from backend.routes.restaurant_employee import router as restaurant_employee_router
from backend.routes.table import router as table_router

# Initialize FastAPI application
app = FastAPI(
    title="Restaurant Management System",
    description="An API for managing restaurant operations including employees, orders, and deliveries.",
    version="1.0.0",
)

app.include_router(address_history_router)
app.include_router(client_router)
app.include_router(deliver_router)
app.include_router(delivery_router)
app.include_router(dish_router)
app.include_router(employment_contract_router)
app.include_router(ingredient_router)
app.include_router(order_router)
app.include_router(person_router)
app.include_router(reservation_router)
app.include_router(restaurant_employee_router)
app.include_router(table_router)

# On application startup, initialize the database
@app.on_event("startup")
def startup_event():
    initialize_database()
    print("Database initialized successfully.")

# Simple health check endpoint
@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "running", "message": "Welcome to the Restaurant Management System API!"}
