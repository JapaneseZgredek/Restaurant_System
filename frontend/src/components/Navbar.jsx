import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();

  if (location.pathname === "/cart") return null; // Do not show Navbar when user is in Cart

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        Restauracja Włoska
        <p className="user-info">Zalogowany jako: Admin</p>
      </div>
      <div className="navbar-links">
        <Link to="/menu">
          <button className="navbar-btn">Menu</button>
        </Link>
        <Link to="/cart">
          <button className="navbar-btn">Przejdź do koszyka</button>
        </Link>
        <Link to="/orders">
          <button className="navbar-btn">Zamówienia</button>
        </Link>
        <Link to="/delivery-orders">
          <button className="navbar-btn">Zamówienia do dostawy</button>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
