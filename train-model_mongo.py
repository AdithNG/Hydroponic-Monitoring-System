from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import json
import random
import time, certifi
from pymongo import MongoClient


# Load MongoDB configuration
with open('config.json') as config_file:
    config = json.load(config_file)

mongo_uri = config['mongo_uri']
client = MongoClient(mongo_uri, tls=True, tlsCAFile=certifi.where())
db = client['Project1']  # Replace with your chosen database name

sensor_data_collection = db['sensor_data']  # Replace with your sensor data collection name

# Function to fetch data from MongoDB
def fetch_data_from_mongodb():
    data = list(sensor_data_collection.find())  # Fetch all data from MongoDB
    return data

# Function to prepare time-series data
def prepare_time_series_data(data, n_steps=1):
    # Create empty lists for inputs (X) and targets (Y)
    X, Y = [], []

    # Convert fetched data into a DataFrame for easier handling
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convert timestamp to datetime format
    df.sort_values(by='timestamp', inplace=True)  # Sort data by timestamp

    # We will use the previous n_steps readings to predict the next one
    for i in range(len(df) - n_steps):
        X.append(df[['temperature', 'humidity', 'ph_level']].iloc[i:i+n_steps].values)
        Y.append(df[['temperature', 'humidity', 'ph_level']].iloc[i+n_steps].values)

    return np.array(X), np.array(Y)

# Function to calculate MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Fetch the data from MongoDB
data = fetch_data_from_mongodb()

# Prepare the data for a time-series prediction model
n_steps = 5  # We'll use the last 5 data points to predict the next one
X, Y = prepare_time_series_data(data, n_steps)

# Split data into training and test sets (80% train, 20% test)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

# Flatten the data for the regression model
X_train_flat = X_train.reshape((X_train.shape[0], -1))
X_test_flat = X_test.reshape((X_test.shape[0], -1))

# Normalize the data for better performance
scaler = StandardScaler()
X_train_flat = scaler.fit_transform(X_train_flat)
X_test_flat = scaler.transform(X_test_flat)

# Simulate epochs by training the model multiple times
n_epochs = 10  # Number of epochs
best_model = None
best_r2 = -np.inf  # Initialize with a very low value

for epoch in range(n_epochs):
    print(f"Epoch {epoch + 1}/{n_epochs}")
    
    # Create and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train_flat, Y_train)
    
    # Make predictions on the test set
    Y_pred = model.predict(X_test_flat)
    
    # Calculate metrics
    mse = mean_squared_error(Y_test, Y_pred)
    mae = mean_absolute_error(Y_test, Y_pred)
    mape = mean_absolute_percentage_error(Y_test, Y_pred)  # MAPE in percentage
    r2 = r2_score(Y_test, Y_pred)  # R-squared score

    # Keep track of the best model based on R²
    if r2 > best_r2:
        best_r2 = r2
        best_model = model

    # Print metrics for the current epoch
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape}%")
    print(f"R-squared (R²): {r2}")

    accuracy = 100 - mape
    print(f"Accuracy: {accuracy}%")

# Final evaluation after the last epoch
print("Training completed.")
print(f"Best R-squared achieved: {best_r2}")

# Save the model and scaler to file
model_filename = 'sensor_model.pkl'
joblib.dump(best_model, model_filename)
print(f"Model saved to {model_filename}")

scaler_filename = 'scaler.pkl'
joblib.dump(scaler, scaler_filename)
print(f"Scaler saved to {scaler_filename}")
