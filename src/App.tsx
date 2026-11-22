import { useState } from "react";

const drinks = [
  { name: "Flat white", price: "3.95", note: "Double shot, silky milk" },
  { name: "Oat latte", price: "4.50", note: "Our most ordered drink" },
  { name: "Cold brew", price: "4.25", note: "Steeped for 18 hours" },
  { name: "Cappuccino", price: "3.95", note: "Classic, with cocoa on top" },
];

const phone = import.meta.env.VITE_ORDER_PHONE;
const hours = import.meta.env.VITE_OPENING_HOURS;

export default function App() {
  const [picked, setPicked] = useState<string | null>(null);
  return (
    <div className="page">
      <header className="hero">
        <h1>Harbor Coffee</h1>
        <p>Fresh coffee by the water, since 2016.</p>
        {hours && <span className="hours">Open {hours}</span>}
      </header>
      <main>
        <h2>Order ahead</h2>
        <div className="grid">
          {drinks.map((d) => (
            <button key={d.name} className={picked === d.name ? "drink picked" : "drink"} onClick={() => setPicked(d.name)}>
              <span className="name">{d.name}</span>
              <span className="note">{d.note}</span>
              <span className="price">${d.price}</span>
            </button>
          ))}
        </div>
        {picked && (
          <div className="ready">
            {picked} it is. {phone ? <>Call <b>{phone}</b> and it'll be ready when you arrive.</> : "See you soon!"}
          </div>
        )}
      </main>
    </div>
  );
}
