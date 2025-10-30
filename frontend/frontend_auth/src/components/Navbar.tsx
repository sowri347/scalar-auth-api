import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("username");
    navigate("/login");
  };

  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-zinc-900 text-white shadow-md">
      <h1 className="text-xl font-bold tracking-wider">
        🛒 <span className="text-gray-200">ShopMate</span>
      </h1>

      <div className="flex gap-6">
        <Link to="/products" className="hover:text-gray-300 transition">
          Products
        </Link>
        <Link to="/cart" className="hover:text-gray-300 transition">
          Cart
        </Link>
        <button
          onClick={logout}
          className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded-lg text-sm transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
