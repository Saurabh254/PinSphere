import axios from "axios";
import { useState, useEffect } from "react";
import { API_URL } from "../constants";
import { Link, useNavigate } from "react-router";
import { GoogleAuth } from "@/components/GoogleAuth";
import { GoogleOAuthProvider } from "@react-oauth/google";

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
const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    rememberMe: false,
  });

  const [error, setError] = useState("");
  const [showToast, setShowToast] = useState(false);

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
    <div className="h-full w-full flex items-center justify-center   md:bg-[#0f172a] relative">
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

      <div className="bg-background dark:border-2 dark:border-white text-primary-foreground rounded-lg  p-4 md:p-6 max-w-lg w-full">
        <div className="flex justify-center mb-6 bg-primary rounded-md">
          <img src="/pin_rect.png" alt="Flowbite Logo" className="h-36" />
        </div>
        <h2 className="text-2xl font-sans text-center mb-6">Welcome back</h2>

        <div className="flex flex-col gap-4 mb-4">
          <GoogleOAuthProvider clientId="738619260855-aad32jgbdkioqjmabv2ot2njssigql3n.apps.googleusercontent.com">
            <GoogleAuth />
          </GoogleOAuthProvider>
          <button className="flex-1 bg-primary hover:bg-opacity-90 py-2 px-6 rounded-lg flex items-center justify-center text-nowrap ">
            <img
              src="https://img.icons8.com/?size=100&id=30840&format=png&color=FFFFFF"
              alt="Apple Logo"
              className="h-5 mr-2"
            />
            Continue with Apple ID
          </button>
        </div>

        <div className="relative flex text-primary dark:text-primary-foreground items-center justify-center mb-4">
          <span className="absolute bg-background px-2 ">or</span>
          <div className="w-full h-px bg-primary dark:bg-primary-foreground"></div>
        </div>

        <div>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-primary dark:text-primary-foreground  text-sm font-medium mb-2"
            >
              Username
            </label>
            <input
              id="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              className="w-full bg-input text-primary-foreground placeholder:text-foreground ring-1 ring-primary rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
          </div>

          <div className="mb-4 autofill:bg-none">
            <label
              htmlFor="password"
              className="block text-sm text-primary dark:text-primary-foreground font-medium mb-2"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              style={{ color: "#000" }}
              className="w-full bg-input text-primary-foreground placeholder:text-foreground  autofill:text-primary ring-primary ring-1 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
          </div>

          <div className="flex items-center justify-between mb-6">
            <label className="flex items-center text-xs text-[#000] dark:text-primary-foreground">
              <input
                type="checkbox"
                id="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                className=" checkbox-primary  checkbox outline-1 outline-primary h-4 w-4 mr-2"
              />
              Remember me
            </label>
            <a
              href="#"
              className="text-color-secondary hover:underline text-xs"
            >
              Forgot password?
            </a>
          </div>

          <button
            type="submit"
            onClick={handleSubmit}
            className="w-full bg-primary text-base-light hover:bg-opacity-90 text-color-primary py-2 px-4 rounded-lg  focus:outline-none focus:ring-2 focus:ring-base-light hover:bg-black cursor-pointer "
          >
            Sign in to your account
          </button>
        </div>

        <p className="text-center text-sm text-primary dark:text-primary-foreground mt-4">
          Don't have an account yet?
          <Link
            to="/signup"
            className="text-primary dark:text-primary-foreground font-semibold ml-1 hover:underline cursor-pointer"
          >
            Sign up here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
