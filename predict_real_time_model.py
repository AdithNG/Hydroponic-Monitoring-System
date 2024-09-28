import joblib
import numpy as np
import pandas as pd
from pymongo import MongoClient
import time

# Load the trained model and scaler from file
model_filename = 'sensor_model.pkl'
model = joblib.load(model_filename)
scaler_filename = 'scaler.pkl'  # Assuming you saved the scaler during training
scaler = joblib.load(scaler_filename)

import time, certifi, json
from pymongo import MongoClient


# Load MongoDB configuration
with open('config.json') as config_file:
    config = json.load(config_file)

mongo_uri = config['mongo_uri']
client = MongoClient(mongo_uri, tls=True, tlsCAFile=certifi.where())
db = client['Project1']  # Replace with your chosen database name


sensor_data_collection = db['sensor_data']  # Replace with your sensor data collection name
predicted_data_collection = db['predicted_data']  # Replace with your predicted data collection name

# Function to fetch the most recent data from MongoDB
def fetch_latest_data(n_steps=5):
    data = list(sensor_data_collection.find().sort('timestamp', -1).limit(n_steps))  # Fetch last n_steps data points

    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df[['temperature', 'humidity', 'ph_level']].values
    else:
        print("No data found in MongoDB.")
        return None

# Real-time prediction loop
while True:
    # Fetch the most recent sensor data
    recent_data = fetch_latest_data()

    if recent_data is not None:
        # Prepare the data for prediction (flatten and scale it)
        recent_data_flat = recent_data.reshape(1, -1)
        recent_data_scaled = scaler.transform(recent_data_flat)  # Use the pre-fitted scaler

        # Make predictions using the loaded model
        prediction = model.predict(recent_data_scaled)
        
        # Display the prediction
        predicted_temperature, predicted_humidity, predicted_ph = prediction[0]
        print(f"Predicted Temperature: {predicted_temperature:.2f}°C, Humidity: {predicted_humidity:.2f}%, pH Level: {predicted_ph:.2f}")

        # Push predictions to MongoDB
        predicted_data_collection.insert_one({
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'predicted_temperature': predicted_temperature,
            'predicted_humidity': predicted_humidity,
            'predicted_ph_level': predicted_ph
        })

    # Wait for a while before making the next prediction (adjust the sleep time as needed)
    time.sleep(5)
