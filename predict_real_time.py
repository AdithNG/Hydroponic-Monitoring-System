import firebase_admin
from firebase_admin import credentials, db
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import time

# Load the trained model and scaler from file
model_filename = 'sensor_model.pkl'
model = joblib.load(model_filename)
scaler_filename = 'scaler.pkl'  # Assuming you saved the scaler during training
scaler = joblib.load(scaler_filename)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'
})

# Function to fetch the most recent data from Firebase
def fetch_latest_data(n_steps=5):
    ref = db.reference('sensor_data')
    data = ref.order_by_key().limit_to_last(n_steps).get()  # Fetch the last n_steps data points

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df[['temperature', 'humidity', 'ph_level']].values
    else:
        print("No data found in Firebase.")
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

        # Optionally, push predictions to Firebase or use them in your visualization
        prediction_ref = db.reference('predicted_data')
        prediction_ref.push({
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'predicted_temperature': predicted_temperature,
            'predicted_humidity': predicted_humidity,
            'predicted_ph_level': predicted_ph
        })

    # Wait for a while before making the next prediction (adjust the sleep time as needed)
    time.sleep(5)
