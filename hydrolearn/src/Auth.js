import { useNavigate } from 'react-router-dom';
import React, { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase"; // Ensure this is pointing to your Firebase setup
import './Auth.css'; // Import your CSS

const Auth = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (email.trim() === "") {
      setError("Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    setError(""); // Clear any previous error messages

    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        console.log("User logged in: ", userCredential.user);
        navigate("/dashboard"); // Navigate to the dashboard
      })
      .catch((error) => {
        console.error("Error logging in: ", error);
        setError(error.message); // Display Firebase-specific error message
      });
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        <h2 className="auth-title">Login</h2>
        <form onSubmit={handleLogin} className="auth-form">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />
          {error && error.includes("email") && (
            <span className="error-message">Format: email@example.com</span>
          )}

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />
          {error && error.includes("Password") && (
            <span className="error-message">Password must be at least 6 characters long.</span>
          )}

          {error && !error.includes("email") && !error.includes("Password") && (
            <span className="error-message">{error}</span>
          )}

          <button type="submit" className="auth-button">Login</button>
        </form>
        <p className="signup-text">
          Don't have an account? <a href="/signup" className="signup-link">Sign Up</a>
        </p>
      </div>
    </div>
  );
};

export default Auth;
