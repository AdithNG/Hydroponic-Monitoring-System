import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'
})

# Function to fetch and count data entries from Firebase
def count_data_entries():
    ref = db.reference('sensor_data')  # Reference to 'sensor_data' node in Firebase
    data = ref.get()  # Fetch all data from Firebase
    if data:
        count = len(data)
        print(f"Number of entries in Firebase: {count}")
    else:
        print("No data found in Firebase.")

# Call the function to count the entries
count_data_entries()
