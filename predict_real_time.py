import firebase_admin
from firebase_admin import credentials, db
import joblib
import pandas as pd
import time

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'
})

# Function to fetch the most recent data from Firebase
def fetch_latest_data(n_steps=1):
    ref = db.reference('sensor_data')
    data = ref.order_by_key().limit_to_last(n_steps).get()  # Fetch the last n_steps data points

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df[['temperature', 'humidity', 'ph_level', 'hydroponic_plant']].values
    else:
        print("No data found in Firebase.")
        return None

# Real-time prediction loop
while True:
    # Fetch the most recent sensor data
    recent_data = fetch_latest_data()

    if recent_data is not None:
        # Prepare the input for the model
        hydroponic_plant_name = recent_data[0][-1]  # Get the hydroponic_plant name from the last row
        input_data = pd.DataFrame({
            'temperature': recent_data[:, 0],
            'humidity': recent_data[:, 1],
            'ph_level': recent_data[:, 2],
            'hydroponic_plant': [hydroponic_plant_name] * recent_data.shape[0]  # Repeat the hydroponic_plant name for the input shape
        })

        # Make predictions using the loaded model
        predictions = model.predict(input_data)

        # Display the predictions
        for pred in predictions:
            predicted_temperature, predicted_humidity, predicted_ph = pred
            print(f"Predicted Conditions for {hydroponic_plant_name} - "
                  f"Temperature: {predicted_temperature:.2f}°C, "
                  f"Humidity: {predicted_humidity:.2f}%, "
                  f"pH Level: {predicted_ph:.2f}")

        # Push predictions to Firebase
        prediction_ref = db.reference('predicted_data')
        for pred in predictions:
            prediction_ref.push({
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'hydroponic_plant': hydroponic_plant_name,
                'predicted_temperature': pred[0],
                'predicted_humidity': pred[1],
                'predicted_ph_level': pred[2]
            })

    # Wait for a while before making the next prediction
    time.sleep(5)
