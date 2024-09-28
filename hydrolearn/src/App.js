// src/App.js

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Auth from "./Auth";  // Import the authentication component
import Home from "./Home";  // Import the new homepage component
import AboutUs from "./AboutUs";  // Import the login component
import Navbar from "./Navbar";

function App() {
    return (
        <Router>
            <div>
            <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} /> 
                    <Route path="/auth" element={<Auth />} />  
                    <Route path="/about" element={<AboutUs />} />

                </Routes>
            </div>
        </Router>
    );
}

export default App;
