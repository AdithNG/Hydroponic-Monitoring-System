import React from 'react';
import './getStarted.css';
import { useNavigate } from 'react-router-dom';

const GetStarted = () => {
  const navigate = useNavigate();

  const handleGoToLogin = () => {
    navigate('/auth'); // Navigating to the login/signup page
  };

  return (
    <div className="get-started-container">
      <h1>Welcome to HydroLearn</h1>
      <p>
        HydroLearn is your trusted system for monitoring hydroponic parameters in real-time.
        Manage your hydroponic garden effectively and efficiently. This guide will help you
        get started on your journey to optimizing plant growth.
      </p>

      <h2>Step-by-Step Guide</h2>
      <ul>
        <li><strong>Step 1:</strong> Create your account and log in.</li>
        <li><strong>Step 2:</strong> Set up your first hydroponic plant by choosing from a list of available crops.</li>
        <li><strong>Step 3:</strong> Start monitoring your plant in real-time with live data updates.</li>
        <li><strong>Step 4:</strong> Set up alerts to stay informed when plant conditions exceed thresholds.</li>
      </ul>

      <h2>Additional Resources</h2>
      <p>
        Learn more about hydroponics and plant care with our educational resources:
      </p>
      <ul>
        <li><a href="/hydroponics-guide">How Hydroponics Works</a></li>
        <li><a href="/best-practices">Best Practices for Hydroponic Gardening</a></li>
        <li><a href="/common-mistakes">Common Mistakes to Avoid in Hydroponics</a></li>
      </ul>

      <button className="dashboard-button" onClick={handleGoToLogin}>
        Login / Signup
      </button>
    </div>
  );
};

export default GetStarted;
