import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react"; // optional spinner icon

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");

  const navigate = useNavigate();

  // ✅ Handle Login
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      localStorage.setItem("authToken", data.access_token);
      localStorage.setItem("username", username);

      navigate("/products");
    } catch (err: any) {
      setError(err.message || "An error occurred during login");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Handle Signup
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccessMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          password,
          email,
          full_name: fullName,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Signup failed");
      }

      await response.json();

      setSuccessMessage("Account created successfully! Please login.");
      setUsername("");
      setPassword("");
      setEmail("");
      setFullName("");

      setTimeout(() => {
        setIsLogin(true);
        setSuccessMessage("");
      }, 2000);
    } catch (err: any) {
      setError(err.message || "An error occurred during signup");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white px-4">
      <div className="w-full max-w-md bg-neutral-900 border border-neutral-800 p-10 rounded-2xl shadow-2xl space-y-8 transition-all">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold tracking-wide text-white">
            {isLogin ? "Sign In" : "Create Account"}
          </h2>
          <p className="text-sm text-gray-400 mt-2">
            {isLogin
              ? "Welcome back! Please login to continue."
              : "Join us by creating a new account."}
          </p>
        </div>

        <form
          className="space-y-5"
          onSubmit={isLogin ? handleLogin : handleSignup}
        >
          <div className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-300 mb-1"
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-black border border-gray-700 text-white placeholder-gray-500 focus:ring-2 focus:ring-white outline-none"
                placeholder="Enter username"
              />
            </div>

            {!isLogin && (
              <>
                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-300 mb-1"
                  >
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-black border border-gray-700 text-white placeholder-gray-500 focus:ring-2 focus:ring-white outline-none"
                    placeholder="Enter email"
                  />
                </div>

                <div>
                  <label
                    htmlFor="fullName"
                    className="block text-sm font-medium text-gray-300 mb-1"
                  >
                    Full Name
                  </label>
                  <input
                    id="fullName"
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-black border border-gray-700 text-white placeholder-gray-500 focus:ring-2 focus:ring-white outline-none"
                    placeholder="Enter full name"
                  />
                </div>
              </>
            )}

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-300 mb-1"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-black border border-gray-700 text-white placeholder-gray-500 focus:ring-2 focus:ring-white outline-none"
                placeholder="Enter password"
              />
            </div>
          </div>

          {error && (
            <div className="bg-red-900/30 border border-red-500 text-red-400 px-4 py-2 rounded-lg text-sm text-center">
              {error}
            </div>
          )}

          {successMessage && (
            <div className="bg-green-900/30 border border-green-500 text-green-400 px-4 py-2 rounded-lg text-sm text-center">
              {successMessage}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 flex justify-center items-center bg-white text-black font-semibold rounded-lg hover:bg-gray-200 transition-all disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2" size={18} />{" "}
                {isLogin ? "Signing in..." : "Creating..."}
              </>
            ) : isLogin ? (
              "Sign In"
            ) : (
              "Sign Up"
            )}
          </button>
        </form>

        <div className="text-center">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
              setSuccessMessage("");
            }}
            className="text-sm text-gray-400 hover:text-white transition-all"
          >
            {isLogin
              ? "Don’t have an account? Sign up"
              : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
