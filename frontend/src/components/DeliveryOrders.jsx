import React, { useState } from "react";
import "./DeliveryOrders.css";

const DeliveryOrders = () => {
  const [orders, setOrders] = useState([
    {
      id: 1,
      status: "ready",
      address: {
        street: "Ulica Włoska",
        buildingNumber: "15",
        city: "Kraków",
        postalCode: "30-001",
        floor: "2",
        notes: "Proszę zadzwonić przed dostawą.",
      },
      client: {
        firstName: "Jan",
        lastName: "Kowalski",
        phone: "123-456-789",
      },
      items: [
        { name: "Pizza Margherita", quantity: 1 },
        { name: "Lasagna", quantity: 1 },
      ],
    },
    {
      id: 2,
      status: "ready",
      address: {
        street: "Via Italia",
        buildingNumber: "8",
        city: "Warszawa",
        postalCode: "00-001",
        floor: "4",
        notes: "",
      },
      client: {
        firstName: "Anna",
        lastName: "Nowak",
        phone: "987-654-321",
      },
      items: [{ name: "Spaghetti Bolognese", quantity: 2 }],
    },
  ]);

  const handleStatusChange = (orderId, newStatus) => {
    setOrders((prevOrders) =>
      prevOrders.map((order) =>
        order.id === orderId ? { ...order, status: newStatus } : order
      )
    );
  };

  const markAsInDelivery = (orderId) => {
    handleStatusChange(orderId, "in delivery");
  };

  const markAsDelivered = (orderId) => {
    handleStatusChange(orderId, "delivered");
  };

  const markAsDelayed = (orderId) => {
    alert(`Zamówienie #${orderId} oznaczone jako opóźnione.`);
  };

  return (
    <div className="delivery-orders-container">
      <h1>Zamówienia do dostarczenia</h1>
      {orders.map((order) => (
        <div
          key={order.id}
          className={`order-card ${
            order.status === "ready" ? "highlight" : ""
          }`}
        >
          <header className="order-header">
            <div>
              <span className="order-title">Zamówienie #{order.id}</span>
              <p className="order-status">Status: {order.status}</p>
            </div>
            <div className="order-actions">
              {order.status === "ready" && (
                <button
                  className="action-button"
                  onClick={() => markAsInDelivery(order.id)}
                >
                  Przyjmij
                </button>
              )}
              {order.status === "in delivery" && (
                <>
                  <button
                    className="action-button"
                    onClick={() => markAsDelivered(order.id)}
                  >
                    Oznacz jako zrealizowane
                  </button>
                  <button
                    className="action-button delayed-button"
                    onClick={() => markAsDelayed(order.id)}
                  >
                    Oznacz jako opóźnione
                  </button>
                </>
              )}
            </div>
          </header>
          <div className="order-details">
            <p>
              <strong>Adres:</strong> {order.address.street}{" "}
              {order.address.buildingNumber}, {order.address.city}{" "}
              {order.address.postalCode}
            </p>
            {order.address.floor && (
                <p>
                  <strong>Piętro:</strong> {order.address.floor}
                </p>
            )}
            {order.address.notes && (
                <p>
                  <strong>Notatki:</strong> {order.address.notes}
                </p>
            )}
            <p>
              <strong>Dane klienta:</strong> {order.client.firstName} {order.client.lastName} -{" "}
              <button
                  className="action-button call-button"
                  onClick={() => alert(`Zadzwoń pod: ${order.client.phone}`)}
              >
                Zadzwoń
              </button>
            </p>
            <table className="order-items">
              <thead>
              <tr>
                <th style={{width: "70%"}}>Nazwa dania</th>
                <th style={{width: "30%"}}>Ilość</th>
              </tr>
              </thead>
              <tbody>
              {order.items.map((item, index) => (
                  <tr key={index}>
                    <td>{item.name}</td>
                    <td>{item.quantity}</td>
                  </tr>
              ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DeliveryOrders;
