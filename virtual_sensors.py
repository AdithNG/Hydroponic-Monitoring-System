import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase Admin SDK
# Replace 'path/to/your-json-file.json' with the actual path to your downloaded JSON file
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'  # Replace with your Firebase database URL
})

# Function to generate random sensor data
def generate_sensor_data():
    temperature = round(random.uniform(18.0, 25.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    ph_level = round(random.uniform(5.5, 7.0), 2)
    return temperature, humidity, ph_level

# Function to push sensor data to Firebase
def push_data_to_firebase(data):
    ref = db.reference('sensor_data')  # Reference to the 'sensor_data' node in Firebase
    ref.push(data)  # Push new sensor data as a child node

# Main loop to continuously generate and push sensor data
if __name__ == "__main__":
    while True:
        temp, humidity, ph = generate_sensor_data()
        
        # Prepare the data to push to Firebase
        sensor_data = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'temperature': temp,
            'humidity': humidity,
            'ph_level': ph
        }
        
        # Push the data to Firebase
        push_data_to_firebase(sensor_data)
        
        # Print the data to confirm it's being pushed
        print(f"Pushed to Firebase: {sensor_data}")
        
        # Wait for 5 seconds before generating the next set of data
        time.sleep(5)
