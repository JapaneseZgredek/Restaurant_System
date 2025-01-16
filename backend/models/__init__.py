from backend.models.person import Person
from backend.models.restaurant_employee import RestaurantEmployee
from backend.models.deliver import Deliver
from backend.models.client import Client
from backend.models.address_history import AddressHistory
from backend.models.dish import Dish
from backend.models.employment_contract import EmploymentContract
from backend.models.ingredient import Ingredient
from backend.models.order import Order
from backend.models.reservation import Reservation
from backend.models.table import Table
from backend.models.delivery import Delivery  # Dodana klasa Delivery

__all__ = [
    "Person",
    "RestaurantEmployee",
    "Deliver",
    "Client",
    "AddressHistory",
    "Dish",
    "EmploymentContract",
    "Ingredient",
    "Order",
    "Reservation",
    "Table",
    "Delivery",  # Dodana klasa Delivery do listy eksportu
]
