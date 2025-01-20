import React, { useState } from "react";
import "./Orders.css";

const Orders = () => {
  const [orders, setOrders] = useState([
    {
      id: 1,
      status: "placed",
      dishes: [
        { name: "Pizza Margherita", quantity: 1 },
        { name: "Lasagna", quantity: 2 },
      ],
    },
    {
      id: 2,
      status: "new",
      dishes: [
        { name: "Pizza Capriciosa", quantity: 1 },
        { name: "Spaghetti Bolognese", quantity: 1 },
      ],
    },
    {
      id: 3,
      status: "ready",
      dishes: [
        { name: "Ravioli", quantity: 3 },
        { name: "Tiramisu", quantity: 1 },
      ],
    },
    {
      id: 4,
      status: "placed",
      dishes: [
        { name: "Pizza Pepperoni", quantity: 1 },
        { name: "Cannoli", quantity: 1 },
      ],
    },
  ]);

  const handleStatusChange = (orderId, newStatus) => {
    setOrders((prevOrders) =>
      prevOrders.map((order) =>
        order.id === orderId ? { ...order, status: newStatus } : order
      )
    );
  };

  const handleAcceptOrder = (orderId) => {
    setOrders((prevOrders) =>
      prevOrders.map((order) =>
        order.id === orderId ? { ...order, status: "new" } : order
      )
    );
  };

  return (
    <div className="orders-container">
      <h1>Zamówienia</h1>
      {orders.length === 0 ? (
        <p>Brak zamówień do wyświetlenia.</p>
      ) : (
        orders.map((order) => (
          <div key={order.id} className="order-card">
            <header className="order-header">
              <div className="order-info">
                <span className="order-title">Zamówienie #{order.id}</span>
                <div className="status-dropdown">
                  <label>Status:</label>
                  <select
                    value={order.status}
                    onChange={(e) =>
                      handleStatusChange(order.id, e.target.value)
                    }
                  >
                    <option value="placed">placed</option>
                    <option value="new">new</option>
                    <option value="ready">ready</option>
                  </select>
                </div>
              </div>
              {order.status === "placed" && (
                <button
                  className="accept-button"
                  onClick={() => handleAcceptOrder(order.id)}
                >
                  Przyjmij
                </button>
              )}
              {order.status === "placed" && <span className="alert-icon">!</span>}
            </header>
            <div className="order-details">
              <table className="order-table">
                <thead>
                  <tr>
                    <th style={{ width: "70%" }}>Potrawa</th>
                    <th style={{ width: "30%" }}>Ilość</th>
                  </tr>
                </thead>
                <tbody>
                  {order.dishes.map((dish, index) => (
                    <tr key={index}>
                      <td>{dish.name}</td>
                      <td>{dish.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default Orders;
