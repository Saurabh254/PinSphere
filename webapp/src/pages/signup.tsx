import axios from "axios";
import React, { useState } from "react";
import { API_URL } from "../constants";
import { Link, useNavigate } from "react-router";
const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    rememberMe: false,
  });

  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [id]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async () => {
    setError(""); // Clear previous errors

    try {
      const res = await axios.post(`${API_URL}/auth/signup`, formData, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (res.status == 204) {
        navigate("/login");
      } else {
        setError(res.data);
      }
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
    <div className="min-h-screen flex items-center justify-center bg-base">
      <div className="bg-white border-1 border-black text-color-primary rounded-lg shadow-lg p-6 max-w-lg w-full">
        <div className="flex justify-center mb-6 bg-base rounded-md">
          <img src="/pin_rect.png" alt="Flowbite Logo" className="h-36" />
        </div>
        <h2 className="text-2xl font-semibold text-center mb-6">
          Create your account
        </h2>

        <div className="flex gap-4 mb-4">
          <button className="flex-1 bg-base hover:bg-opacity-90 text-primary-content py-2 px-4 rounded-lg flex items-center justify-center text-nowrap font-semibold">
            <img
              src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
              alt="Google Logo"
              className="h-5 mr-2"
            />
            Sign up with Google
          </button>
          <button className="flex-1 bg-base hover:bg-opacity-90 text-primary-content py-2 px-4 rounded-lg flex items-center justify-center text-nowrap font-semibold">
            <img
              src="https://img.icons8.com/?size=100&id=30840&format=png&color=FFFFFF"
              alt="Apple Logo"
              className="h-5 mr-2"
            />
            Sign up with Apple
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
              style={{ color: error.includes("username") ? "red" : "black" }}
            >
              Username
            </label>
            <input
              id="username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="new-password"
              placeholder="Enter your username"
              className="w-full bg-color-accent text-color-accent-content rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
            {error.includes("username") && (
              <p className="text-red-500 text-sm mt-1">{error}</p>
            )}
          </div>

          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-2"
              style={{ color: error.includes("email") ? "red" : "black" }}
            >
              Email
            </label>
            <input
              id="email"
              value={formData.email}
              onChange={handleChange}
              autoComplete="new-password"
              placeholder="Enter your email"
              className="w-full bg-color-accent text-color-accent-content rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
            {error.includes("email") && (
              <p className="text-red-500 text-sm mt-1">{error}</p>
            )}
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
              autoComplete="new-password"
              placeholder="Enter your password"
              className="w-full bg-color-accent text-color-accent-content rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
            {error.includes("password") && (
              <p className="text-red-500 text-sm mt-1">{error}</p>
            )}
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
            Sign up for your account
          </button>
        </div>

        <p className="text-center text-sm text-color-primary-content mt-4">
          Already have an account?{" "}
          <Link
            to="/login"
            className="text-color-secondary hover:underline font-semibold cursor-pointer"
          >
            Login here
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
