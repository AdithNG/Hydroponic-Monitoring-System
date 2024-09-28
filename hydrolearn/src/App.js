import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import React from "react";
import Auth from "./Auth";  // Import the authentication component
import Home from "./Home";  // Import the new homepage component
import AboutUs from "./AboutUs";  // Import the About Us component
import Navbar from "./Navbar";
import ContactUs from "./ContactUs";

function App() {
    return (
        <Router>
            <AppContent />  {/* Move content to another component */}
        </Router>
    );
}

function AppContent() {
    const location = useLocation();

    return (
        <div>
            {/* Show the Navbar only if the path is not '/auth' */}
            {location.pathname !== '/auth' && <Navbar />}
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/auth" element={<Auth />} />
                <Route path="/about" element={<AboutUs />} />
                <Route path="/contact" element={<ContactUs />} />
                {/* Add other routes here */}
            </Routes>
        </div>
    );
}

export default App;
