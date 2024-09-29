import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; 
import Home from "./Home";  
import AboutUs from "./AboutUs";  
import Navbar from "./Navbar";
import ContactUs from "./ContactUs";
import SignUp from "./SignUp";
import Auth from './Auth';
import Dashboard from "./Dashboard";

function App() {
    return (
        <Router>
            <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<AboutUs />} />
                    <Route path="/contact" element={<ContactUs />} />
                    <Route path="/signup" element={<SignUp />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/signup" element={<SignUp />} />
                    <Route path="/auth" element={<Auth />} />

                </Routes>
        </Router>
    );
}

export default App;
