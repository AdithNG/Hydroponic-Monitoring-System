import React from "react";
import { useNavigate } from "react-router-dom";
import './Home.css';  // Assuming the CSS for the navbar is in Home.css

const Navbar = () => {
    const navigate = useNavigate();

    return (
        <nav className="navbar">
            <div className="nav-left">
                {/* Wrap the text in a clickable div */}
                <h2 onClick={() => navigate('/')} style={{cursor: 'pointer'}}>HydroLearn</h2>
            </div>
            <div className="nav-right">
                <button className="nav-button" onClick={() => navigate('/about')}>About Us</button>
                <button className="nav-button" onClick={() => navigate('/contact')}>Contact Us</button>
                <button className="nav-button" onClick={() => navigate('/auth')}>Login / Signup</button>
            </div>
        </nav>
    );
};


export default Navbar;

