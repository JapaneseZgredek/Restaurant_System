import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Cart.css";

const Cart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useState([]);
  const [paymentMethod, setPaymentMethod] = useState("");
  const [deliveryType, setDeliveryType] = useState("pickup");
  const [address, setAddress] = useState({
    street: "",
    buildingNumber: "",
    apartmentNumber: "",
    city: "",
    postalCode: "",
    floor: "",
    staircase: "",
  });

  useEffect(() => {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    setCartItems(cart);
  }, []);

  const totalPrice = cartItems.reduce((sum, item) => sum + item.price, 0);

  const handlePaymentChange = (e) => {
    setPaymentMethod(e.target.value);
  };

  const handleDeliveryChange = (e) => {
    setDeliveryType(e.target.value);
  };

  const handleAddressChange = (e) => {
    const { name, value } = e.target;
    setAddress((prevAddress) => ({
      ...prevAddress,
      [name]: value,
    }));
  };

  const handleOrder = () => {
    if (cartItems.length === 0) {
      alert("Koszyk jest pusty. Nie można złożyć zamówienia.");
      return;
    }

    if (deliveryType === "delivery" && (!address.street || !address.buildingNumber || !address.city || !address.postalCode)) {
      alert("Proszę uzupełnić wszystkie wymagane pola adresu dostawy.");
      return;
    }

    alert(
      `Zamówienie złożone!\nMetoda płatności: ${paymentMethod}\nTyp dostawy: ${deliveryType}${
        deliveryType === "delivery"
          ? `\nAdres dostawy: ${address.street} ${address.buildingNumber}${
              address.apartmentNumber ? `/${address.apartmentNumber}` : ""
            }, ${address.city} ${address.postalCode}`
          : ""
      }`
    );
    localStorage.removeItem("cart");
    setCartItems([]);
    navigate("/menu");
  };

  const removeFromCart = (uniqueId) => {
    const updatedCart = cartItems.filter((item) => item.uniqueId !== uniqueId);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
    setCartItems(updatedCart);
  };

  return (
    <div className="cart-container">
      <header className="cart-header">
        <h1>Koszyk</h1>
        <div className="header-buttons">
          <button className="btn btn-back" onClick={() => navigate("/menu")}>
            Powrót do menu
          </button>
        </div>
      </header>

      <section className="cart-items">
        <h2>Twoje zamówienie</h2>
        {cartItems.map((item, index) => (
          <div key={index} className="cart-item">
            <span className="cart-item-name">{item.name}</span>
            <span className="cart-item-price">{item.price} PLN</span>
            <button
              className="remove-btn"
              onClick={() => removeFromCart(item.uniqueId)}
            >
              ❌
            </button>
          </div>
        ))}
        {cartItems.length === 0 && (
          <p className="empty-cart-message">Koszyk jest pusty.</p>
        )}
      </section>

      <section className="cart-delivery">
        <h2>Opcje dostawy</h2>
        <div className="delivery-options">
          <label>
            <input
              type="radio"
              name="deliveryType"
              value="pickup"
              checked={deliveryType === "pickup"}
              onChange={handleDeliveryChange}
            />
            Odbiór własny
          </label>
          <label>
            <input
              type="radio"
              name="deliveryType"
              value="delivery"
              checked={deliveryType === "delivery"}
              onChange={handleDeliveryChange}
            />
            Dostawa
          </label>
        </div>
      </section>

      {deliveryType === "delivery" && (
        <section className="cart-address">
          <h2>Adres dostawy</h2>
          <form className="address-form">
            <div className="form-group">
              <label>Ulica</label>
              <input
                type="text"
                name="street"
                placeholder="Wpisz ulicę"
                value={address.street}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Numer budynku</label>
              <input
                type="text"
                name="buildingNumber"
                placeholder="Wpisz numer budynku"
                value={address.buildingNumber}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Numer mieszkania (opcjonalne)</label>
              <input
                type="text"
                name="apartmentNumber"
                placeholder="Wpisz numer mieszkania"
                value={address.apartmentNumber}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Miasto</label>
              <input
                type="text"
                name="city"
                placeholder="Wpisz miasto"
                value={address.city}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Kod pocztowy</label>
              <input
                type="text"
                name="postalCode"
                placeholder="Wpisz kod pocztowy"
                value={address.postalCode}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Piętro (opcjonalne)</label>
              <input
                type="text"
                name="floor"
                placeholder="Wpisz piętro"
                value={address.floor}
                onChange={handleAddressChange}
              />
            </div>
            <div className="form-group">
              <label>Klatka (opcjonalne)</label>
              <input
                type="text"
                name="staircase"
                placeholder="Wpisz klatkę"
                value={address.staircase}
                onChange={handleAddressChange}
              />
            </div>
          </form>
        </section>
      )}

      <section className="cart-payment">
        <h2>Płatność</h2>
        <div className="payment-options">
          {["Gotówka", "Karta", "Przelew", "Blik"].map((method) => (
            <label key={method} className="payment-option">
              <input
                type="radio"
                name="payment"
                value={method}
                checked={paymentMethod === method}
                onChange={handlePaymentChange}
              />
              {method}
            </label>
          ))}
        </div>
      </section>

      <footer className="cart-footer">
        <span className="total-price">Razem: {totalPrice.toFixed(2)} PLN</span>
        <button
          className="btn order-btn"
          onClick={handleOrder}
          disabled={!paymentMethod || cartItems.length === 0}
        >
          Złóż zamówienie
        </button>
      </footer>
    </div>
  );
};

export default Cart;
