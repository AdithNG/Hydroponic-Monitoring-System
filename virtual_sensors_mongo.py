import json
import random
import time, certifi
from pymongo import MongoClient


# Load MongoDB configuration
with open('config.json') as config_file:
    config = json.load(config_file)

mongo_uri = config['mongo_uri']
client = MongoClient(mongo_uri, tls=True, tlsCAFile=certifi.where())
mongo_db = client['Project1']  # Replace with your chosen database name
mongo_collection = mongo_db['sensor_data']  # Collection name for sensor data

# Function to generate random sensor data
def generate_sensor_data():
    temperature = round(random.uniform(18.0, 25.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    ph_level = round(random.uniform(5.5, 7.0), 2)
    return temperature, humidity, ph_level

# Function to push sensor data to MongoDB
def push_data_to_mongodb(data):
    mongo_collection.insert_one(data)  # Insert the sensor data into the collection

# Main loop to continuously generate and push sensor data
if __name__ == "__main__":
    while True:
        temp, humidity, ph = generate_sensor_data()
        
        # Prepare the data to push to MongoDB
        sensor_data = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'temperature': temp,
            'humidity': humidity,
            'ph_level': ph
        }
        
        # Push the data to MongoDB
        push_data_to_mongodb(sensor_data)
        
        # Print the data to confirm it's being pushed
        print(f"Pushed to MongoDB: {sensor_data}")
        
        # Wait for 5 seconds before generating the next set of data
        time.sleep(5)
