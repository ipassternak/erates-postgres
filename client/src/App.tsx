import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import { HomePage } from "./pages/home";
import { AccountPage } from "./pages/account";
import { LoginPage } from "./pages/login";
import { RegisterPage } from "./pages/register";
import { WalletsPage } from "./pages/wallets";
import { TransactionsPage } from "./pages/transactions";

function App() {
  const drawerButtons = [
    { name: "E-Rates", path: "/" },
    { name: "Account", path: "/account" },
    { name: "Wallets", path: "/wallets" },
    { name: "Transactions", path: "/transactions" },
  ];

  return (
    <Router>
      <div className="layout">
        <div className="mainDrawer">
          {drawerButtons.map((button) => (
            <Link to={button.path} className="drawerButton" key={button.name}>
              {button.name}
            </Link>
          ))}
        </div>
        <div className="mainContent">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/account" element={<AccountPage />} />
            <Route path="/wallets" element={<WalletsPage />} />
            <Route path="/transactions" element={<TransactionsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<div>404</div>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
