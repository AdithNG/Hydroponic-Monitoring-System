import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK (Make sure you provide the correct credentials file and database URL)
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'  # Replace with your Firebase URL
})

def fetch_data_from_firebase():
    """
    Fetches the most recent sensor data from Firebase and returns it as a pandas DataFrame.
    """
    try:
        # Reference to the 'sensor_data' node in Firebase
        ref = db.reference('sensor_data')

        # Fetch all data from Firebase
        data = ref.get()

        if data:
            # Convert the data into a pandas DataFrame
            df = pd.DataFrame.from_dict(data, orient='index')

            # Convert the 'timestamp' column to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Sort the DataFrame by timestamp to ensure correct order
            df.sort_values(by='timestamp', inplace=True)

            # Reset index for clean DataFrame
            df.reset_index(drop=True, inplace=True)

            # Return the processed DataFrame
            return df
        else:
            print("No data found in Firebase.")
            return None

    except Exception as e:
        print(f"Error fetching data from Firebase: {e}")
        return None
    
# Train separate models for each crop and store them
def train_models_per_crop():
    # Fetch and preprocess the data from Firebase
    df = fetch_data_from_firebase()

    # Check if data exists
    if df is None or df.empty:
        print("No data to train on.")
        return

    # Initialize an empty dictionary to store models for each crop
    models = {}
    r2_scores = {}

    # List of crop names (assuming 'hydroponic_plant' is the column in df)
    crops = df['hydroponic_plant'].unique()

    for crop in crops:
        # Filter data for the current crop
        crop_data = df[df['hydroponic_plant'] == crop]

        # Prepare the feature and target columns
        X = crop_data[['temperature', 'humidity', 'ph_level']]  # Features (without hydroponic_plant)
        y = crop_data[['temperature', 'humidity', 'ph_level']]  # Targets

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest model for the current crop
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Store the model in the dictionary
        models[crop] = model

        # Evaluate the model and store R² scores
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        r2_scores[crop] = r2
        print(f"Model for {crop} - R² score: {r2}")

        # Save the model for the specific crop
        model_filename = f'random_forest_model_{crop}.pkl'
        joblib.dump(model, model_filename)
        print(f"Model for {crop} saved as {model_filename}")

    # Save the feature columns (useful for real-time predictions)
    train_columns = list(X.columns)
    with open('train_columns.pkl', 'wb') as f:
        pickle.dump(train_columns, f)
        print("Feature columns saved in train_columns.pkl")

    return models, r2_scores

if __name__ == "__main__":
    # Train and store separate models for each crop
    models, scores = train_models_per_crop()

    # Display the R² scores for each crop
    if scores:
        for crop, score in scores.items():
            print(f"R² score for {crop}: {score}")
    else:
        print("No models were trained.")
