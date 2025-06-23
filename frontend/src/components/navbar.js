import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar__brand">
        <Link to="/dashboard" className="navbar__logo">
          <span role="img" aria-label="FlashRisk" style={{marginRight: "0.5rem"}}>⚡</span>
          FlashRisk
        </Link>
      </div>
      <ul className="navbar__links">
        <li>
          <Link to="/dashboard" className={location.pathname === "/dashboard" ? "active" : ""}>
            Dashboard
          </Link>
        </li>
        {/* Add more links as your app grows */}
        <li>
          <a href="https://github.com/A-P-U-R-B-O/FlashRisk" target="_blank" rel="noopener noreferrer">
            GitHub
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
