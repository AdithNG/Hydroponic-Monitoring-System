import joblib
import pandas as pd
import time
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'  # Replace with your Firebase URL
})

# Load the trained models for each crop (ensure the models are stored correctly)
models = {
    'Apple': joblib.load('random_forest_model_Apple.pkl'),
    'Banana': joblib.load('random_forest_model_Banana.pkl'),
    'Blackgram': joblib.load('random_forest_model_Blackgram.pkl'),
    'Cotton': joblib.load('random_forest_model_Cotton.pkl'),
    'Orange': joblib.load('random_forest_model_Orange.pkl'),
    'Papaya': joblib.load('random_forest_model_Papaya.pkl')
}

# Load the feature columns used during training
with open('train_columns.pkl', 'rb') as f:
    train_columns = joblib.load(f)

# Function to fetch the most recent sensor data for a specific plant from Firebase
def fetch_recent_data(plant_name, n_steps=1):
    ref = db.reference('sensor_data')
    data = ref.order_by_child('hydroponic_plant').equal_to(plant_name).limit_to_last(n_steps).get()

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df[['temperature', 'humidity', 'ph_level', 'hydroponic_plant']].values
    else:
        print(f"No data found for {plant_name} in Firebase.")
        return None

# Prepare input data for prediction (one-hot encode the plant type)
def prepare_input_data(recent_data):
    input_data = pd.DataFrame({
        'temperature': [recent_data[0][0]],
        'humidity': [recent_data[0][1]],
        'ph_level': [recent_data[0][2]],
        'hydroponic_plant': [recent_data[0][3]]
    })

    # One-hot encode the hydroponic_plant column
    input_data = pd.get_dummies(input_data, columns=['hydroponic_plant'])

    # Align the columns with the training columns (add missing columns with default values)
    for column in train_columns:
        if column not in input_data.columns:
            input_data[column] = 0

    input_data = input_data[train_columns]  # Ensure column order matches
    return input_data

# Function to push predicted data to Firebase
def push_predicted_data(plant_name, predictions):
    ref = db.reference('predicted_data')  # Reference to 'predicted_data' node in Firebase
    prediction_data = {
        'hydroponic_plant': plant_name,
        'predicted_temperature': predictions[0],
        'predicted_humidity': predictions[1],
        'predicted_ph_level': predictions[2],
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    ref.push(prediction_data)
    print(f"Pushed predicted data for {plant_name}: {prediction_data}")

# Real-time prediction loop for all crops
def predict_for_all_crops():
    crops = ['Apple', 'Banana', 'Blackgram', 'Cotton', 'Orange', 'Papaya']
    
    while True:
        for crop in crops:
            # Fetch the most recent sensor data for the crop
            recent_data = fetch_recent_data(crop)
            
            if recent_data is not None:
                # Prepare input data for the model
                input_data = prepare_input_data(recent_data)
                
                # Make predictions using the corresponding model for the crop
                model = models[crop]
                predictions = model.predict(input_data)[0]
                
                # Push the predicted data to Firebase
                push_predicted_data(crop, predictions)

        # Wait before making the next set of predictions
        time.sleep(10)  # Adjust the sleep time as needed

if __name__ == "__main__":
    predict_for_all_crops()
