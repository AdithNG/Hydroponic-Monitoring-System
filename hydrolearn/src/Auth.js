import React, { useState } from 'react';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import './Auth.css';

const Auth = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailError, setEmailError] = useState('');
    const [passwordError, setPasswordError] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        const auth = getAuth();

        // Clear any previous errors
        setEmailError('');
        setPasswordError('');

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setEmailError('Format: email@example.com');
            return;
        }

        // Validate password: minimum 6 characters, 1 uppercase and 1 lowercase letter
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z]).{6,}$/;
        if (!passwordRegex.test(password)) {
            if (password.length < 6) {
                setPasswordError('Password must be at least 6 characters long');
            } else {
                setPasswordError('Password must contain both uppercase and lowercase letters');
            }
            return;
        }

        // Perform Firebase authentication
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                alert('Login successful!');
                console.log('User logged in:', userCredential.user);
            })
            .catch((error) => {
                const errorMessage = error.message;
                alert(errorMessage);
            });
    };

    return (
        <div className="auth-page"> {/* Scoped background */}
            <div className="auth-container">
                <h1 className="auth-title">Login</h1>
                <form className="auth-form" onSubmit={handleLogin}>
                    <label htmlFor="email">Email</label>
                    <input 
                        type="email"
                        id="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    {emailError && <div className="email-hint">{emailError}</div>}

                    <label htmlFor="password">Password</label>
                    <input 
                        type="password"
                        id="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    {passwordError && <div className="email-hint">{passwordError}</div>}

                    <button type="submit" className="auth-button">Login</button>
                </form>

                <div className="signup-text">
                    Don't have an account? <a href="/signup" className="signup-link">Sign Up</a>
                </div>
            </div>
        </div>
    );
};

export default Auth;
