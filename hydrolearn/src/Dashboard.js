import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import { getDatabase, ref, query, orderByChild, equalTo, limitToLast, onValue } from "firebase/database";
import { auth } from './firebase';  // Import your Firebase authentication setup
import LineChart from './LineChart'; // Assuming the LineChart component is ready

const crops = ["Apple", "Banana", "Blackgram", "Cotton", "Orange", "Papaya"]; // List of crop options

const Dashboard = () => {
  const [sensorData, setSensorData] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState(""); // To store the selected crop
  const [error, setError] = useState("");
  const [userName, setUserName] = useState(""); // Store the user's name

  // Fetch the user's name from Firebase Authentication
  useEffect(() => {
    const currentUser = auth.currentUser;
    if (currentUser) {
      setUserName(currentUser.displayName || currentUser.email); // Set the user's display name or email
    }
  }, []);

  const handleCropChange = (e) => {
    setSelectedCrop(e.target.value); // Set the selected crop
  };

  useEffect(() => {
    if (selectedCrop) {
      // Fetch data from Firebase Realtime Database for the selected crop
      const db = getDatabase();
      const sensorRef = query(ref(db, 'sensor_data'), orderByChild('hydroponic_plant'), equalTo(selectedCrop), limitToLast(20));

      onValue(sensorRef, (snapshot) => {
        const data = snapshot.val();
        if (data) {
          const formattedData = Object.values(data).map((entry) => ({
            temperature: entry.temperature,
            humidity: entry.humidity,
            pHLevel: entry.ph_level,
            timestamp: entry.timestamp
          }));
          setSensorData(formattedData);
        } else {
          setSensorData([]);
          setError(`No data found for ${selectedCrop}`);
        }
      });
    }
  }, [selectedCrop]);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to HydroLearn Dashboard, {userName}</h1>
        <select className="crop-dropdown" onChange={handleCropChange}>
          <option value="">Select a Crop</option>
          {crops.map((crop) => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>
      </header>

      <section className="real-time-monitoring">
        <h2>Real-Time Monitoring for {selectedCrop || 'No crop selected'}</h2>
        {selectedCrop && sensorData.length > 0 ? (
          <>
            <LineChart data={sensorData.map(d => d.temperature)} label="Temperature" />
            <LineChart data={sensorData.map(d => d.humidity)} label="Humidity" />
            <LineChart data={sensorData.map(d => d.pHLevel)} label="pH Level" />
            <p className="timestamp">Last updated: {sensorData[sensorData.length - 1].timestamp}</p>
          </>
        ) : (
          <p>{error || 'Please select a crop to view the data.'}</p>
        )}
      </section>

      <footer className="dashboard-footer">
        <p>HydroLearn &copy; 2024 | Created by the HydroLearn Team</p>
      </footer>
    </div>
  );
};

export default Dashboard;
