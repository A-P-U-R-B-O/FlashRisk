import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import "./styles/main.css";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Add more routes here as your app grows */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

// Minimal NotFound component (inline for now)
function NotFound() {
  return (
    <main style={{ padding: "4rem", textAlign: "center" }}>
      <h2>404 – Page Not Found</h2>
      <p>The page you are looking for does not exist.</p>
      <a href="/dashboard" style={{ color: "#457b9d", textDecoration: "underline" }}>
        Go to Dashboard
      </a>
    </main>
  );
}

export default App;
