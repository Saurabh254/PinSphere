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
          setError("User Already Exists");
        } else {
          setError(err.response.data.detail);
        }
      } else {
        setError("Network error. Please check your connection.");
      }
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center  w-full">
      <div className="bg-background  rounded-lg  p-6 max-w-lg w-full">
        <div className="flex justify-center  mb-6 bg-primary rounded-md">
          <img src="/pin_rect.png" alt="Flowbite Logo" className="h-36" />
        </div>
        <h2 className="text-2xl font-semibold text-center mb-2">
          Create your account
        </h2>
        {error && (
          <div className="w-full mb-6  text-error-content bg-error rounded-md px-2 text-center py-2">
            {error}
          </div>
        )}

        <div>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-primary-foreground  text-sm font-medium mb-2"
              style={{
                color: error.includes("username") ? "red" : "var(--foreground)",
              }}
            >
              Username
            </label>
            <input
              id="username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="new-password"
              placeholder="Enter your username"
              className="w-full light:bg-white bg-input text-foreground rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
            />
            {error.includes("username") && (
              <p className="text-red-500 text-sm mt-1">{error}</p>
            )}
          </div>

          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-2"
              style={{
                color: error.includes("email") ? "red" : "var(--foreground)",
              }}
            >
              Email
            </label>
            <input
              id="email"
              value={formData.email}
              onChange={handleChange}
              autoComplete="new-password"
              placeholder="Enter your email"
              className="w-full bg-input text-foreground rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
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
              className="w-full bg-input text-foreground rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-color-secondary"
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
                className="checkbox bg-input  text-primary h-4 w-4 mr-2"
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
            className="w-full bg-primary text-primary-foreground hover:bg-opacity-90 text-color-primary-content py-2 px-4 rounded-lg font-medium focus:outline-none focus:ring-2 focus:ring-base-light"
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
