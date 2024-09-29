import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import firebase_admin
from firebase_admin import db, credentials
import joblib
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'  # Your Firebase URL
})

# Load the trained model
model = joblib.load('random_forest_model.pkl')

# Initialize lists to store real sensor data
timestamps = []
temperatures = []
humidities = []
ph_levels = []
plants = []  # List to store plant names

# Initialize lists to store predicted data
predicted_timestamps = []
predicted_temperatures = []
predicted_humidities = []
predicted_ph_levels = []

# Alert threshold values
temp_upper_limit = 30.0
temp_lower_limit = 18.0
humidity_upper_limit = 65.0
humidity_lower_limit = 40.0
ph_upper_limit = 7.0
ph_lower_limit = 5.5

# Function to fetch real sensor data from Firebase
def fetch_data_from_firebase():
    ref = db.reference('sensor_data')  # Reference to 'sensor_data' node in Firebase
    data = ref.get()  # Fetch all data from Firebase
    return data

# Process and format the real sensor data
def process_data(data):
    timestamps.clear()
    temperatures.clear()
    humidities.clear()
    ph_levels.clear()
    plants.clear()  # Clear previous plant data

    for key, entry in data.items():
        # Convert the timestamp string to datetime
        timestamps.append(datetime.datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"))
        temperatures.append(float(entry['temperature']))
        humidities.append(float(entry['humidity']))
        ph_levels.append(float(entry['ph_level']))
        plants.append(entry['hydroponic_plant'])  # Store the plant name

# Function to update the plot
def update_graph(i):
    # Fetch and process the real sensor data
    data = fetch_data_from_firebase()
    process_data(data)

    # Prepare input for prediction (last fetched data)
    if temperatures and humidities and ph_levels and plants:
        last_plant_name = plants[-1]  # Get the most recent plant name
        input_data = pd.DataFrame({
            'temperature': [temperatures[-1]],
            'humidity': [humidities[-1]],
            'ph_level': [ph_levels[-1]],
            'hydroponic_plant': [last_plant_name]  # Use the most recent plant name
        })

        # Make predictions using the loaded model
        predictions = model.predict(input_data)

        # Store predicted values
        predicted_temperature, predicted_humidity, predicted_ph = predictions[0]
        predicted_timestamps.append(datetime.datetime.now())
        predicted_temperatures.append(predicted_temperature)
        predicted_humidities.append(predicted_humidity)
        predicted_ph_levels.append(predicted_ph)

    # Limit to the last 20 entries
    max_entries = 20
    real_timestamps = timestamps[-max_entries:]
    real_temperatures = temperatures[-max_entries:]
    real_humidities = humidities[-max_entries:]
    real_ph_levels = ph_levels[-max_entries:]

    predicted_timestamps_limited = predicted_timestamps[-max_entries:]
    predicted_temperatures_limited = predicted_temperatures[-max_entries:]
    predicted_humidities_limited = predicted_humidities[-max_entries:]
    predicted_ph_levels_limited = predicted_ph_levels[-max_entries:]

    # Update the real sensor data lines
    temp_line.set_data(real_timestamps, real_temperatures)
    humidity_line.set_data(real_timestamps, real_humidities)
    ph_line.set_data(real_timestamps, real_ph_levels)

    # Update the predicted data lines
    pred_temp_line.set_data(predicted_timestamps_limited, predicted_temperatures_limited)
    pred_humidity_line.set_data(predicted_timestamps_limited, predicted_humidities_limited)
    pred_ph_line.set_data(predicted_timestamps_limited, predicted_ph_levels_limited)

    # Update the x-axis limits
    ax.set_xlim(min(real_timestamps), max(real_timestamps))

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Initialize the lines for real sensor data
temp_line, = ax.plot([], [], label="Temperature (C)", color='red')
humidity_line, = ax.plot([], [], label="Humidity (%)", color='blue')
ph_line, = ax.plot([], [], label="pH Level", color='green')

# Initialize the lines for predicted data
pred_temp_line, = ax.plot([], [], label="Predicted Temperature (C)", linestyle='-.', marker='o', color='orange')
pred_humidity_line, = ax.plot([], [], label="Predicted Humidity (%)", linestyle='-.', marker='x', color='purple')
pred_ph_line, = ax.plot([], [], label="Predicted pH Level", linestyle='-.', marker='^', color='brown')

# Add alert threshold lines
ax.axhline(y=temp_upper_limit, color='red', linestyle='--', label='Temperature Limit')
ax.axhline(y=temp_lower_limit, color='red', linestyle='--')
ax.axhline(y=humidity_upper_limit, color='blue', linestyle='--', label='Humidity Limit')
ax.axhline(y=humidity_lower_limit, color='blue', linestyle='--')
ax.axhline(y=ph_upper_limit, color='green', linestyle='--', label='pH Level Limit')
ax.axhline(y=ph_lower_limit, color='green', linestyle='--')

# Add legends and formatting
ax.legend(loc='upper left')
ax.set_title('Real-Time Sensor Data with Predictions and Alerts Over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Values')
plt.xticks(rotation=45)  # Rotate timestamp labels for readability

# Create the animation
ani = animation.FuncAnimation(fig, update_graph, interval=5000)  # Update every 5 seconds (5000 ms)

# Show the animated plot
plt.tight_layout()
plt.show()
