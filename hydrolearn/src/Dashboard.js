import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import { getDatabase, ref, onValue } from "firebase/database";
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const [sensorData, setSensorData] = useState({
        temperature: null,
        humidity: null,
        pHLevel: null,
        timestamp: null
    });
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch data from Firebase Realtime Database
        const db = getDatabase();
        const sensorRef = ref(db, 'sensor_data');
        onValue(sensorRef, (snapshot) => {
            const data = snapshot.val();
            if (data) {
                // Assuming the latest sensor data is stored at the last node in 'sensor_data'
                const latestEntry = Object.keys(data).pop();
                setSensorData({
                    temperature: data[latestEntry].temperature,
                    humidity: data[latestEntry].humidity,
                    pHLevel: data[latestEntry].ph_level,
                    timestamp: data[latestEntry].timestamp
                });
            }
        });
    }, []);

    const handleLogout = () => {
        // Add your logout logic here (e.g., Firebase signOut)
        navigate('/auth');
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>Welcome to HydroLearn Dashboard</h1>
                <button className="logout-button" onClick={handleLogout}>Log Out</button>
            </header>

            <section className="real-time-monitoring">
                <h2>Real-Time Monitoring</h2>
                <div className="sensor-data">
                    <div className="sensor">
                        <h3>Temperature</h3>
                        <p>{sensorData.temperature ? `${sensorData.temperature}°C` : 'Loading...'}</p>
                    </div>
                    <div className="sensor">
                        <h3>Humidity</h3>
                        <p>{sensorData.humidity ? `${sensorData.humidity}%` : 'Loading...'}</p>
                    </div>
                    <div className="sensor">
                        <h3>pH Level</h3>
                        <p>{sensorData.pHLevel ? `${sensorData.pHLevel}` : 'Loading...'}</p>
                    </div>
                </div>
                <p className="timestamp">Last updated: {sensorData.timestamp ? sensorData.timestamp : 'Loading...'}</p>
            </section>

            <section className="data-visualization">
                <h2>Data Visualization</h2>
                <p>Graphs will go here (implement with chart.js or another graphing library)</p>
            </section>

            <footer className="dashboard-footer">
                <p>HydroLearn &copy; 2024 | Created by the HydroLearn Team</p>
            </footer>
        </div>
    );
};

export default Dashboard;
