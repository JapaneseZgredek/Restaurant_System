import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Menu from "./components/Menu";
import Cart from "./components/Cart";
import Orders from "./components/Orders";
import DeliveryOrders from "./components/DeliveryOrders"; // Import komponentu Orders

const App = () => {
  const [dishes, setDishes] = useState([]);
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const fetchDishes = async () => {
      try {
        const response = await fetch("http://localhost:8000/dish/dishes/all-with-relations");
        const data = await response.json();
        setDishes(data);
      } catch (error) {
        console.error("Błąd podczas pobierania danych:", error);
      }
    };

    fetchDishes();
  }, []);

  const handleRemoveFromCart = (uniqueId) => {
    const updatedCart = cartItems.filter((item) => item.uniqueId !== uniqueId);
    setCartItems(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  const handlePlaceOrder = (paymentMethod) => {
    console.log(`Order placed with payment method: ${paymentMethod}`);
    setCartItems([]);
    localStorage.removeItem("cart");
  };

  return (
    <Router>
      <div className="app">
        <Navbar />
        <Routes>
          <Route path="/menu" element={<Menu dishes={dishes} />} />
          <Route
            path="/cart"
            element={
              <Cart
                cartItems={cartItems}
                onRemove={handleRemoveFromCart}
                onPlaceOrder={handlePlaceOrder}
              />
            }
          />
          <Route path="/orders" element={<Orders />} />
          <Route path="/delivery-orders" element={<DeliveryOrders />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
