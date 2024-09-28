import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Auth from "./Auth";  
import Home from "./Home";  
import AboutUs from "./AboutUs";  
import Navbar from "./Navbar";
import ContactUs from "./ContactUs";

function App() {
    return (
        <Router>
            <div>
                {/* Navbar should be visible on all pages except auth */}
                <Routes>
                    <Route path="/auth" element={<Auth />} />
                    <Route path="/*" element={<Navbar />} />
                </Routes>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/about" element={<AboutUs />} />
                    <Route path="/contact" element={<ContactUs />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
