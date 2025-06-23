import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/main.css";

// Optionally enable React.StrictMode for highlighting potential problems
const rootElement = document.getElementById("root");

const root = createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
