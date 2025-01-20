import React from "react";
import DishCard from "./DishCard";
import "./Menu.css";

const Menu = ({ dishes }) => {
  return (
    <div className="menu">
      <h1 className="menu-title">Menu</h1>
      <div className="menu-list">
        {dishes.map((dish) => (
          <DishCard key={dish.id} dish={dish} />
        ))}
      </div>
    </div>
  );
};

export default Menu;
