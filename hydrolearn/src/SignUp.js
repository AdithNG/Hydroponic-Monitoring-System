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

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email validation regex

  const handleSignUp = (e) => {
    e.preventDefault();

    if (name.trim() === "") {
      alert("Please enter your name.");
      return;
    }

    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      alert("Password must be at least 6 characters long.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
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
              alert("User registered successfully!");
              navigate("/dashboard"); // Navigate to dashboard after successful signup
            }).catch((error) => {
              console.error("Error saving user details to database:", error);
              alert("Error saving user details to the database.");
            });
          })
          .catch((error) => {
            console.error("Error updating user profile: ", error);
            alert("Error updating user profile: " + error.message);
          });
      })
      .catch((error) => {
        console.error("Error signing up: ", error);
        alert("Error signing up: " + error.message); // Display Firebase-specific error message via alert
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

          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            required
          />

          <label htmlFor="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
          />

          <button 
            type="submit" 
            className="signup-button"
            disabled={!name || !emailRegex.test(email) || password.length < 6 || password !== confirmPassword}
          >
            Sign Up
          </button>
        </form>
        <p className="login-text">
          Already have an account? <a href="/auth" className="login-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default SignUp;
