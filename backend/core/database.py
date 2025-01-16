from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///./database.db"

# Create database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Function to initialize the database
def initialize_database():
    from backend.models import (
        person,
        restaurant_employee,
        deliver,
        delivery,
        client,
        address_history,
        dish,
        employment_contract,
        ingredient,
        order,
        reservation,
        table,
    )
    Base.metadata.create_all(bind=engine)
