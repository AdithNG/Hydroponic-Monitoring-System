import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { auth } from './firebase'; // Assuming you have Firebase auth setup

const Navbar = ({ user }) => {
  const navigate = useNavigate();
  const location = useLocation(); // Hook to get the current route

  const handleLogout = () => {
    auth.signOut()
      .then(() => {
        // Sign-out successful.
        navigate('/'); // Redirect to home or login page after logout
      })
      .catch((error) => {
        console.error('Error logging out: ', error);
      });
  };

  // Navigation handler for other buttons
  const handleNavigation = (path) => {
    navigate(path);
  };

  // Determine if the current path is the dashboard
  const isDashboard = location.pathname === '/dashboard';

  return (
    <nav className="navbar">
      <div className="nav-left">
        <Link to="/" style={{ textDecoration: 'none', color: '#3498db' }}>
          <h2>HydroLearn</h2>
        </Link>
      </div>
      <div className="nav-right">
        {/* Always show About Us and Contact Us buttons */}
        <button className="nav-button" onClick={() => handleNavigation('/about')}>
          About Us
        </button>
        <button className="nav-button" onClick={() => handleNavigation('/contact')}>
          Contact Us
        </button>

        {/* Conditionally show the button only when on dashboard */}
        {isDashboard ? (
          <button className="nav-button" onClick={handleLogout}>
            Logout
          </button>
        ) : (
          <button className="nav-button" onClick={() => handleNavigation('/auth')}>
            Login / Signup
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
