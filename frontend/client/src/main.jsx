import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// Defer heavy background until after first paint
requestAnimationFrame(() => {
  document.body.classList.add("bg-ready");
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
