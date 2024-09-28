import React, { useState } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';  // Import authentication functions
import { auth } from './firebase';  // Import the initialized auth instance from firebase.js


const Auth = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isLogin) {
            // Login existing user
            signInWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    console.log("Logged in:", userCredential.user);
                })
                .catch((error) => console.error("Error:", error.message));
        } else {
            // Create new user
            createUserWithEmailAndPassword(auth, email, password)
                .then((userCredential) => {
                    console.log("Signed up:", userCredential.user);
                })
                .catch((error) => console.error("Error:", error.message));
        }
    };

    return (
        <div>
            <h1>{isLogin ? 'Login' : 'Sign Up'}</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    type="email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Email" 
                    required 
                />
                <input 
                    type="password" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    placeholder="Password" 
                    required 
                />
                <button type="submit">{isLogin ? 'Login' : 'Sign Up'}</button>
            </form>
            <button onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Create an account' : 'Already have an account? Log in'}
            </button>
        </div>
    );
};


export default Auth;
