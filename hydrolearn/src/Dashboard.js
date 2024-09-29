import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import { getDatabase, ref, query, orderByChild, equalTo, limitToLast, onValue } from "firebase/database";
import { auth } from './firebase';
import LineChart from './LineChart'; // Assuming the LineChart component is ready
import Notes from './Notes';

const crops = ["Apple", "Banana", "Blackgram", "Cotton", "Orange", "Papaya"];

const Dashboard = () => {
  const [sensorData, setSensorData] = useState([]);
  const [predictedData, setPredictedData] = useState([]); // State to store predicted data
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
      const db = getDatabase();

      // Fetch sensor data for the selected crop
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
          setError(`No sensor data found for ${selectedCrop}`);
        }
      });

      // Fetch predicted data for the selected crop
      const predictedRef = query(ref(db, 'predicted_data'), orderByChild('hydroponic_plant'), equalTo(selectedCrop), limitToLast(20));
      onValue(predictedRef, (snapshot) => {
        const data = snapshot.val();
        if (data) {
          const formattedPredictedData = Object.values(data).map((entry) => ({
            predictedTemperature: entry.predicted_temperature, // Adjusted to match the database
            predictedHumidity: entry.predicted_humidity,       // Adjusted to match the database
            predictedPhLevel: entry.predicted_ph_level,        // Adjusted to match the database
            timestamp: entry.timestamp,
          }));
          setPredictedData(formattedPredictedData);
        } else {
          setPredictedData([]);
          setError(`No predicted data found for ${selectedCrop}`);
        }
      });
    }
  }, [selectedCrop]);

  // Get the latest sensor data (most recent entry)
  const latestData = sensorData.length > 0 ? sensorData[sensorData.length - 1] : null;

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <h1>Welcome to HydroSense Dashboard, {userName}<br /><br /></h1>
        
        {/* Crop Dropdown */}
        <select className="crop-dropdown" onChange={handleCropChange}>
          <option value="">Select a Crop</option>
          {crops.map((crop) => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>
      </header>

      {/* Display current values if available */}
      {latestData && (
        <div className="current-values">
          <h3>Current Values for {selectedCrop}</h3>
          <div className="value-boxes">
            <div className="value-box">
              <p>Temperature</p>
              <p>{latestData.temperature}°C</p>
            </div>
            <div className="value-box">
              <p>Humidity</p>
              <p>{latestData.humidity}%</p>
            </div>
            <div className="value-box">
              <p>pH Level</p>
              <p>{latestData.pHLevel}</p>
            </div>
          </div>
        </div>
      )}

      {/* Main Dashboard Sections */}
      <div className="dashboard-main-content">
        {/* Real-Time Monitoring Section */}
        <section className="real-time-monitoring">
          <h2>Real-Time Monitoring for {selectedCrop || 'No crop selected'}</h2>
          {selectedCrop && sensorData.length > 0 ? (
            <>
              <LineChart 
                actualData={sensorData.map(d => d.temperature)} 
                predictedData={predictedData.map(d => d.predictedTemperature)} 
                label="Temperature" 
                timestamps={sensorData.map(d => d.timestamp)} 
              />
              <LineChart 
                actualData={sensorData.map(d => d.humidity)} 
                predictedData={predictedData.map(d => d.predictedHumidity)} 
                label="Humidity" 
                timestamps={sensorData.map(d => d.timestamp)} 
              />
              <LineChart 
                actualData={sensorData.map(d => d.pHLevel)} 
                predictedData={predictedData.map(d => d.predictedPhLevel)} 
                label="pH Level" 
                timestamps={sensorData.map(d => d.timestamp)} 
              />
              <p className="timestamp">Last updated: {sensorData[sensorData.length - 1].timestamp}</p>
            </>
          ) : (
            <p>{error || 'Please select a crop to view the data.'}</p>
          )}
        </section>

        {/* Notes Section */}
        <section className="notes-section">
          <Notes />
        </section>
      </div>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>HydroSense &copy; 2024 | Created by the HydroSense Team</p>
      </footer>
    </div>
  );
};

export default Dashboard;
