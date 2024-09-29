import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createUserWithEmailAndPassword, updateProfile } from "firebase/auth";
import { auth } from "./firebase"; // Assuming you have your firebase setup in a separate file
import { getDatabase, ref, set } from "firebase/database"; // For saving in Realtime Database

import './SignUp.css'; // This should import your SignUp specific styles

const SignUp = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignUp = (e) => {
    e.preventDefault();

    if (name.trim() === "") {
      setError("Please enter your name.");
      return;
    }

    if (email.trim() === "") {
      setError("Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setError(""); // Clear any previous error messages

    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        const user = userCredential.user;

        // Update the user profile with the name
        updateProfile(user, { displayName: name })
          .then(() => {
            // Save additional details to Firebase Realtime Database
            const db = getDatabase(); // Or use Firestore instead
            set(ref(db, 'users/' + user.uid), {
              uid: user.uid,
              name: name,
              email: user.email
            }).then(() => {
              console.log('User details saved to Firebase Database');
              navigate("/dashboard"); // Navigate to dashboard after successful signup
            }).catch((error) => {
              console.error("Error saving user details to database:", error);
            });
          })
          .catch((error) => {
            console.error("Error updating user profile: ", error);
            setError(error.message); // Display Firebase-specific error message
          });
      })
      .catch((error) => {
        console.error("Error signing up: ", error);
        setError(error.message); // Display Firebase-specific error message
      });
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-container">
        <h2 className="signup-title">Sign Up</h2>
        <form onSubmit={handleSignUp} className="signup-form">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            required
          />
          {error && error.includes("name") && (
            <span className="error-message">Please enter your name.</span>
          )}

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

          <label htmlFor="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
          />
          {error && error.includes("match") && (
            <span className="error-message">Passwords do not match.</span>
          )}

          {error && !error.includes("email") && !error.includes("Password") && !error.includes("match") && (
            <span className="error-message">{error}</span>
          )}

          <button type="submit" className="signup-button">Sign Up</button>
        </form>
        <p className="login-text">
          Already have an account? <a href="/auth" className="login-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default SignUp;
