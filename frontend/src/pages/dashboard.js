body {
  margin: 0;
  font-family: 'Roboto', Arial, sans-serif;
  background: #f7f9fa;
  color: #1d3557;
  min-height: 100vh;
}

a {
  color: #457b9d;
  text-decoration: none;
  transition: color 0.2s;
}

a:hover {
  color: #e63946;
  text-decoration: underline;
}

main {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

button, .btn {
  background: #e63946;
  color: #fff;
  font-weight: 700;
  border: none;
  border-radius: 28px;
  padding: 0.7rem 1.7rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

button:hover, .btn:hover {
  background: #a4161a;
}

/* Navbar styles (used by components/Navbar.js) */
.navbar {
  background: linear-gradient(90deg, #457b9d, #1d3557 80%);
  color: #fff;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.navbar__brand .navbar__logo {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
}

.navbar__links {
  list-style: none;
  display: flex;
  gap: 1.6rem;
  margin: 0;
  padding: 0;
}

.navbar__links li {
  display: inline;
}

.navbar__links a {
  color: #f1faee;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 0.3rem 0.7rem;
  border-radius: 18px;
  transition: background 0.2s, color 0.2s;
}

.navbar__links a.active,
.navbar__links a:hover {
  background: #f1faee;
  color: #1d3557;
}

/* Responsive styles */
@media (max-width: 700px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    padding: 1rem;
  }
  .navbar__brand {
    margin-bottom: 0.7rem;
  }
  .navbar__links {
    gap: 1rem;
    font-size: 1rem;
  }
  main {
    padding: 1rem 0.5rem;
  }
}

/* Dashboard and general card styles */
.card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(38,50,56,0.07);
  padding: 1.5rem;
  margin-bottom: 1.6rem;
}

@media (max-width: 500px) {
  .card {
    padding: 1rem;
  }
}
