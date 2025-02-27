import axios from "axios";
import { useState, useEffect } from "react";
import { API_URL } from "../constants";
import { Link, useNavigate } from "react-router";

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rememberMe: false,
  });

  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

  interface FormData {
    username: string;
    password: string;
    rememberMe: boolean;
  }

  interface ChangeEvent {
    target: {
      id: string;
      value: string;
      type: string;
      checked: boolean;
    };
  }

  // Effect to handle showing and automatically hiding the toast
  useEffect(() => {
    if (error) {
      setShowToast(true);
      const timer = setTimeout(() => {
        setShowToast(false);
      }, 3000); // Hide toast after 3 seconds

      return () => clearTimeout(timer);
    }
  }, [error]);

  const handleChange = (e: ChangeEvent) => {
    const { id, value, type, checked } = e.target;
    setFormData((prev: FormData) => ({
      ...prev,
      [id]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async () => {
    setError(""); // Clear previous errors

    try {
      const res = await axios.post(`${API_URL}/auth/login`, formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("access_token", res.data.access_token);
      navigate("/");
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        if (err.response.status === 404) {
          setError("Invalid username");
        } else if (err.response.status === 400) {
          setError("Incorrect password");
        } else {
          setError("Something went wrong. Please try again.");
        }
      } else {
        setError("Network error. Please check your connection.");
      }
    }
  };
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-base relative">
      {/* DaisyUI Toast */}
      {showToast && (
        <div className="toast toast-top toast-end z-50">
          <div className="alert alert-error">
            <div>
              <span>{error}</span>
            </div>
          </div>
        </div>
      )}

      <div className="bg-white border-1 border-black text-color-primary rounded-lg shadow-lg p-6 max-w-lg w-full">
        <div className="flex justify-center mb-6 bg-base rounded-md">
          <img src="/pin_rect.png" alt="Flowbite Logo" className="h-36" />
        </div>
        <h2 className="text-2xl font-semibold text-center mb-6">
          Welcome back
        </h2>

        <div className="flex gap-4 mb-4">
          <button className="flex-1 bg-base hover:bg-opacity-90 text-primary-content py-2 px-4 rounded-lg flex items-center justify-center text-nowrap font-semibold">
            <img
              src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
              alt="Google Logo"
              className="h-5 mr-2"
            />
            Log in with Google
          </button>
          <button className="flex-1 bg-base hover:bg-opacity-90 text-primary-content py-2 px-4 rounded-lg flex items-center justify-center text-nowrap font-semibold">
            <img
              src="https://img.icons8.com/?size=100&id=30840&format=png&color=FFFFFF"
              alt="Apple Logo"
              className="h-5 mr-2"
            />
            Log in with Apple
          </button>
        </div>

        <div className="relative flex items-center justify-center mb-4">
          <span className="absolute bg-white px-2">or</span>
          <div className="w-full h-px bg-base"></div>
        </div>

        <div>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-sm font-medium mb-2"
            >
              Username
            </label>
            <input
              id="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              className="w-full bg-color-accent text-color-accent-content rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
          </div>

          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium mb-2"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              className="w-full bg-color-accent text-color-accent-content rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
          </div>

          <div className="flex items-center justify-between mb-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                id="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                className="form-checkbox bg-color-accent text-color-accent-content h-4 w-4 mr-2"
              />
              Remember me
            </label>
            <a
              href="#"
              className="text-color-secondary hover:underline text-sm"
            >
              Forgot password?
            </a>
          </div>

          <button
            type="submit"
            onClick={handleSubmit}
            className="w-full bg-base text-base-light hover:bg-opacity-90 text-color-primary-content py-2 px-4 rounded-lg font-medium focus:outline-none focus:ring-2 focus:ring-base-light"
          >
            Sign in to your account
          </button>
        </div>

        <p className="text-center text-sm text-color-primary-content mt-4">
          Don't have an account yet?{" "}
          <Link
            to="/signup"
            className="text-color-secondary hover:underline font-semibold cursor-pointer"
          >
            Sign up here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
