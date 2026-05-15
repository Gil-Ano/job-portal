import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-green-600">
          Get Hired
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link
                to="/jobs"
                className="text-gray-600 hover:text-green-600 text-sm"
              >
                Browse Jobs
              </Link>
              {user.role === "employer" ? (
                <Link
                  to="/employer"
                  className="text-gray-600 hover:text-green-600 text-sm"
                >
                  Dashboard
                </Link>
              ) : (
                <Link
                  to="/dashboard"
                  className="text-gray-600 hover:text-green-600 text-sm"
                >
                  Dashboard
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="text-sm text-red-500 hover:text-red-700"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="text-gray-600 hover:text-green-600 text-sm"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-green-700"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
