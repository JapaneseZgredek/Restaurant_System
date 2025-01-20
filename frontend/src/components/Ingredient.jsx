import React, { useState } from "react";
import "./Ingredient.css";

const Ingredient = ({ name }) => {
  const [quantity, setQuantity] = useState(1);

  const increment = (e) => {
    e.stopPropagation(); // Stops closing dropdown
    setQuantity(quantity + 1);
  };

  const decrement = (e) => {
    e.stopPropagation(); // Stops closing dropdown
    if (quantity > 0) {
      setQuantity(quantity - 1);
    }
  };

  return (
    <li className="ingredient-item">
      <span className="ingredient-name">{name}</span>
      <div className="ingredient-controls">
        <button className="control-button decrement" onClick={decrement}>
          -
        </button>
        <span className="quantity">{quantity}</span>
        <button className="control-button increment" onClick={increment}>
          +
        </button>
      </div>
    </li>
  );
};

export default Ingredient;
