import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
from pymongo import MongoClient

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

# Initialize lists to store real sensor data
timestamps = []
temperatures = []
humidities = []
ph_levels = []

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

# Function to fetch real sensor data from MongoDB
def fetch_data_from_mongodb():
    data = list(sensor_data_collection.find())  # Fetch all data from MongoDB
    return data

# Function to fetch predicted data from MongoDB
def fetch_predicted_data_from_mongodb():
    data = list(predicted_data_collection.find())  # Fetch all predicted data from MongoDB
    return data

# Process and format the real sensor data
def process_data(data):
    timestamps.clear()
    temperatures.clear()
    humidities.clear()
    ph_levels.clear()

    for entry in data:
        # Convert the timestamp string to datetime
        timestamps.append(datetime.datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"))
        temperatures.append(float(entry['temperature']))
        humidities.append(float(entry['humidity']))
        ph_levels.append(float(entry['ph_level']))

# Process and format the predicted data
def process_predicted_data(data):
    predicted_timestamps.clear()
    predicted_temperatures.clear()
    predicted_humidities.clear()
    predicted_ph_levels.clear()

    for entry in data:
        # Convert the timestamp string to datetime
        predicted_timestamps.append(datetime.datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S"))
        predicted_temperatures.append(float(entry['predicted_temperature']))
        predicted_humidities.append(float(entry['predicted_humidity']))
        predicted_ph_levels.append(float(entry['predicted_ph_level']))

# Function to update the plot
def update_graph(i):
    # Fetch and process the real sensor data
    data = fetch_data_from_mongodb()
    process_data(data)
    
    # Fetch and process the predicted data
    predicted_data = fetch_predicted_data_from_mongodb()
    process_predicted_data(predicted_data)

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

    # Update the hover annotation
    annot.set_visible(False)

# Mouse event function for interactive hover annotations
def on_hover(event):
    if event.inaxes == ax:
        for line in [temp_line, humidity_line, ph_line, pred_temp_line, pred_humidity_line, pred_ph_line]:
            contains, index = line.contains(event)
            if contains:
                annot.xy = (event.xdata, event.ydata)
                annot.set_text(f"{line.get_label()}: {event.ydata:.2f}")
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return

        # Check for limits
        if abs(event.ydata - temp_upper_limit) < 0.5:
            annot.xy = (event.xdata, temp_upper_limit)
            annot.set_text(f"Temperature Upper Limit: {temp_upper_limit:.2f}")
            annot.set_visible(True)
        elif abs(event.ydata - temp_lower_limit) < 0.5:
            annot.xy = (event.xdata, temp_lower_limit)
            annot.set_text(f"Temperature Lower Limit: {temp_lower_limit:.2f}")
            annot.set_visible(True)
        elif abs(event.ydata - humidity_upper_limit) < 0.5:
            annot.xy = (event.xdata, humidity_upper_limit)
            annot.set_text(f"Humidity Upper Limit: {humidity_upper_limit:.2f}")
            annot.set_visible(True)
        elif abs(event.ydata - humidity_lower_limit) < 0.5:
            annot.xy = (event.xdata, humidity_lower_limit)
            annot.set_text(f"Humidity Lower Limit: {humidity_lower_limit:.2f}")
            annot.set_visible(True)
        elif abs(event.ydata - ph_upper_limit) < 0.05:
            annot.xy = (event.xdata, ph_upper_limit)
            annot.set_text(f"pH Upper Limit: {ph_upper_limit:.2f}")
            annot.set_visible(True)
        elif abs(event.ydata - ph_lower_limit) < 0.05:
            annot.xy = (event.xdata, ph_lower_limit)
            annot.set_text(f"pH Lower Limit: {ph_lower_limit:.2f}")
            annot.set_visible(True)
        else:
            annot.set_visible(False)

        fig.canvas.draw_idle()

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

# Create an annotation object
annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

# Add legends and formatting
ax.legend(loc='upper left')
ax.set_title('Real-Time Sensor Data with Predictions and Alerts Over Time')
ax.set_xlabel('Time')
ax.set_ylabel('Values')
plt.xticks(rotation=45)  # Rotate timestamp labels for readability

# Create the animation
ani = animation.FuncAnimation(fig, update_graph, interval=5000)  # Update every 5 seconds (5000 ms)

# Connect the hover event to the function
fig.canvas.mpl_connect("motion_notify_event", on_hover)

# Show the animated plot
plt.tight_layout()
plt.show()
