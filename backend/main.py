from fastapi import FastAPI
from backend.core.database import initialize_database

# Initialize FastAPI application
app = FastAPI(
    title="Restaurant Management System",
    description="An API for managing restaurant operations including employees, orders, and deliveries.",
    version="1.0.0",
)

# On application startup, initialize the database
@app.on_event("startup")
def startup_event():
    initialize_database()
    print("Database initialized successfully.")

# Simple health check endpoint
@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "running", "message": "Welcome to the Restaurant Management System API!"}
