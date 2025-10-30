import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const authToken = localStorage.getItem("authToken");

  // If no token found, redirect to login
  if (!authToken) {
    return <Navigate to="/login" replace />;
  }

  // Token exists — allow access
  return <>{children}</>;
};

export default ProtectedRoute;
