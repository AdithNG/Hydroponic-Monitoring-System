import firebase_admin
from firebase_admin import credentials, db
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'
})

# Function to fetch all sensor data from Firebase
def fetch_all_data():
    ref = db.reference('sensor_data')
    data = ref.get()  # Fetch all data points

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df
    else:
        print("No data found in Firebase.")
        return None

# Load the dataset from Firebase
data = fetch_all_data()

if data is not None:
    # Prepare the features and target variables
    X = data[['temperature', 'humidity', 'ph_level', 'hydroponic_plant']]  # Ensure 'hydroponic_plant' column exists
    y = data[['temperature', 'humidity', 'ph_level']]

    # Create a column transformer for one-hot encoding the hydroponic_plant names
    column_transformer = ColumnTransformer(
        transformers=[
            ('hydroponic_plant', OneHotEncoder(), ['hydroponic_plant'])
        ],
        remainder='passthrough'
    )

    # Create a pipeline with a Random Forest model
    pipeline = Pipeline(steps=[
        ('preprocessor', column_transformer),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Train the model on the entire dataset
    pipeline.fit(X, y)

    # Save the model
    joblib.dump(pipeline, 'random_forest_model.pkl')
