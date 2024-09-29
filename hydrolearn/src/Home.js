import React from "react";
import { useNavigate } from "react-router-dom";
import './Home.css';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div>
            {/* Main Welcome Section */}
            <div className="welcome-section">
                <h1 className="title">Welcome to HydroLearn</h1>
                <p className="subtitle">Your reliable system for monitoring hydroponic parameters in real-time. Manage your hydroponic garden effectively and efficiently.</p>
                <button className="get-started-button" onClick={() => navigate('/getStarted')}>Get Started</button>
            </div>

            {/* Key Features Section */}
            <section className="features-section">
                <h2 className="features-title">Key Features</h2>
                <div className="features">
                    <div className="feature">
                        <h3>Real-Time Monitoring</h3>
                        <p>Get up-to-date information on key hydroponic parameters like temperature, humidity, and pH.</p>
                    </div>
                    <div className="feature">
                        <h3>Data Visualization</h3>
                        <p>View trends and insights from historical data with intuitive graphs and charts.</p>
                    </div>
                    <div className="feature">
                        <h3>Smart Alerts</h3>
                        <p>Receive notifications when your system's conditions exceed safe levels.</p>
                    </div>
                    <div className="feature">
                        <h3>Predictive Analytics</h3>
                        <p>HydroLearn predicts future system conditions, helping you prevent issues before they arise.</p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <p>HydroLearn &copy; 2024 | Created by the HydroLearn Team</p>
            </footer>
        </div>
    );
};

export default Home;
