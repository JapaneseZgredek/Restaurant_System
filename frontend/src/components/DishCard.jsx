import React, { useState } from "react";
import Ingredient from "./Ingredient";
import Modal from "./Modal";
import { v4 as uuidv4 } from "uuid";
import "./DishCard.css";

const DishCard = ({ dish }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleDetails = () => {
    setIsOpen(!isOpen);
  };

  const handleOrder = (e) => {
    e.stopPropagation();
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const updatedCart = [...cart, { ...dish, uniqueId: uuidv4() }];
    localStorage.setItem("cart", JSON.stringify(updatedCart));
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div className={`dish-card ${isOpen ? "open" : ""}`} onClick={toggleDetails}>
        <div className="dish-header">
          <h2 className="dish-name">{dish.name}</h2>
          <div className="dish-info">
            <span className="dish-price">{dish.price} PLN</span>
            <button className="order-button" onClick={handleOrder}>
              Zamów
            </button>
          </div>
        </div>
        {isOpen && (
          <div className="dish-details" onClick={(e) => e.stopPropagation()}>
            <p className="dish-description">{dish.description}</p>
            <h3 className="ingredients-title">Składniki:</h3>
            <ul className="ingredients-list">
              {dish.ingredients.map((ingredient) => (
                <Ingredient key={ingredient.id} name={ingredient.name} amount={ingredient.amount} />
              ))}
            </ul>
          </div>
        )}
      </div>

      {isModalOpen && (
        <Modal onClose={closeModal}>
          <h2>Dodano do koszyka</h2>
          <div className="modal-buttons">
            <button onClick={closeModal}>Kontynuuj zakupy</button>
            <button onClick={() => (window.location.href = "/cart")}>Przejdź do koszyka</button>
          </div>
        </Modal>
      )}
    </>
  );
};

export default DishCard;
