import firebase_admin
from firebase_admin import credentials, db
import random
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'  # Replace with your Firebase database URL
})

# Function to generate random sensor data for each plant
def generate_sensor_data(plant_name):
    # Randomly generate sensor readings
    temperature = round(random.uniform(18.0, 25.0), 2)
    humidity = round(random.uniform(40.0, 70.0), 2)
    ph_level = round(random.uniform(5.5, 7.0), 2)

    # Return the data along with the plant name
    return {
        'hydroponic_plant': plant_name,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'temperature': temperature,
        'humidity': humidity,
        'ph_level': ph_level
    }

# Function to push sensor data to Firebase
def push_data_to_firebase(data):
    ref = db.reference('sensor_data')  # Reference to the 'sensor_data' node in Firebase
    ref.push(data)  # Push new sensor data as a child node

# Main loop to continuously generate and push sensor data for all plants
if __name__ == "__main__":
    plant_names = ["Apple", "Banana", "Blackgram", "Cotton", "Orange", "Papaya"]
    
    while True:
        for plant in plant_names:
            # Generate data for the current plant
            sensor_data = generate_sensor_data(plant)
            
            # Push the data to Firebase
            push_data_to_firebase(sensor_data)
            
            # Print the data to confirm it's being pushed
            print(f"Pushed to Firebase: {sensor_data}")
        
        # Wait for 5 seconds before generating the next set of data
        time.sleep(5)
