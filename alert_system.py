import firebase_admin
from firebase_admin import credentials, db
import time
import sendgrid
from sendgrid.helpers.mail import Mail
import pandas as pd
from twilio.rest import Client

# SendGrid API Key (replace with your own)
SENDGRID_API_KEY = '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'

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC1ca1f54ffee2088bc187d474ddbe057d'  # Replace with your Twilio Account SID
TWILIO_AUTH_TOKEN = 'be0e4a4cc17a6a2d7ec1349c23fdf718'    # Replace with your Twilio Auth Token
TWILIO_PHONE_NUMBER = '+18559174810'            # Your Twilio phone number
TO_PHONE_NUMBER = '+16673454053'                # Temporary phone number (use from user later)

# Define alert thresholds for actual and predicted values
TEMP_HIGH = 30.0
TEMP_LOW = 18.0

HUMIDITY_HIGH = 65.0
HUMIDITY_LOW = 40.0

PH_HIGH = 7.0
PH_LOW = 5.0

# Initialize Firebase Admin SDK
cred = credentials.Certificate("hydrolearn-f411f-firebase-adminsdk-p51y1-e521470dd6.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hydrolearn-f411f-default-rtdb.firebaseio.com/'
})

# Function to send email alerts via SendGrid
def send_email_alert(subject, body, to_email="adithnishanth@gmail.com"):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    # Ensure HTML breaks are used for newlines
    formatted_body = body.replace("\n", "<br>")  
    message = Mail(
        from_email="adith@neuroleapmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=formatted_body  # Use the formatted body with HTML breaks
    )
    try:
        response = sg.send(message)
        print(f"Email sent with status code {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
# Function to send SMS alerts via Twilio
def send_sms_alert(message_body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

# Function to fetch the most recent sensor data from Firebase
def fetch_latest_actual_data():
    ref = db.reference('sensor_data')
    data = ref.order_by_key().limit_to_last(1).get()  # Fetch the latest data point

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df.iloc[-1].to_dict()  # Return the latest row as a dictionary
    else:
        print("No data found in Firebase.")
        return None

# Function to fetch the most recent predicted data from Firebase
def fetch_latest_predicted_data():
    ref = db.reference('predicted_data')
    data = ref.order_by_key().limit_to_last(1).get()  # Fetch the latest predicted data point

    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
        return df.iloc[-1].to_dict()  # Return the latest row as a dictionary
    else:
        print("No predicted data found in Firebase.")
        return None

# Function to check actual and predicted data and send alerts
def check_alerts(actual, predicted):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    team_name = "HydroLearn Team" 

    # Check actual temperature
    if actual['temperature'] > TEMP_HIGH:
        message = (f"ALERT: High Temperature Detected!\n\n"
                   f"At {timestamp}, the temperature exceeded the safety limit of {TEMP_HIGH}°C.\n"
                   f"Current Temperature: {actual['temperature']}°C\n\n"
                   f"Please take immediate action to prevent damage to your hydroponics system.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: High Temperature Alert!", message)
        send_sms_alert(message)
    elif actual['temperature'] < TEMP_LOW:
        message = (f"ALERT: Low Temperature Detected!\n\n"
                   f"At {timestamp}, the temperature dropped below the safety limit of {TEMP_LOW}°C.\n"
                   f"Current Temperature: {actual['temperature']}°C\n\n"
                   f"Please take immediate action to ensure optimal conditions.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: Low Temperature Alert!", message)
        send_sms_alert(message)

    # Check predicted temperature
    if predicted['predicted_temperature'] > TEMP_HIGH:
        message = (f"WARNING: High Predicted Temperature!\n\n"
                   f"At {timestamp}, the predicted temperature is expected to exceed the safety limit of {TEMP_HIGH}°C.\n"
                   f"Predicted Temperature: {predicted['predicted_temperature']}°C\n\n"
                   f"Stay alert and monitor the conditions closely.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: High Predicted Temperature!", message)
        send_sms_alert(message)
    elif predicted['predicted_temperature'] < TEMP_LOW:
        message = (f"WARNING: Low Predicted Temperature!\n\n"
                   f"At {timestamp}, the predicted temperature is expected to drop below the safety limit of {TEMP_LOW}°C.\n"
                   f"Predicted Temperature: {predicted['predicted_temperature']}°C\n\n"
                   f"Prepare to adjust the system accordingly.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: Low Predicted Temperature!", message)
        send_sms_alert(message)

    # Check actual humidity
    if actual['humidity'] > HUMIDITY_HIGH:
        message = (f"ALERT: High Humidity Detected!\n\n"
                   f"At {timestamp}, the humidity exceeded the safety limit of {HUMIDITY_HIGH}%.\n"
                   f"Current Humidity: {actual['humidity']}%\n\n"
                   f"Please take action to avoid potential system damage.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: High Humidity Alert!", message)
        send_sms_alert(message)
    elif actual['humidity'] < HUMIDITY_LOW:
        message = (f"ALERT: Low Humidity Detected!\n\n"
                   f"At {timestamp}, the humidity dropped below the safety limit of {HUMIDITY_LOW}%.\n"
                   f"Current Humidity: {actual['humidity']}%\n\n"
                   f"Ensure optimal conditions are restored immediately.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: Low Humidity Alert!", message)
        send_sms_alert(message)

    # Check predicted humidity
    if predicted['predicted_humidity'] > HUMIDITY_HIGH:
        message = (f"WARNING: High Predicted Humidity!\n\n"
                   f"At {timestamp}, the predicted humidity is expected to exceed the safety limit of {HUMIDITY_HIGH}%.\n"
                   f"Predicted Humidity: {predicted['predicted_humidity']}%\n\n"
                   f"Stay alert for potential issues and monitor closely.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: High Predicted Humidity!", message)
        send_sms_alert(message)
    elif predicted['predicted_humidity'] < HUMIDITY_LOW:
        message = (f"WARNING: Low Predicted Humidity!\n\n"
                   f"At {timestamp}, the predicted humidity is expected to drop below the safety limit of {HUMIDITY_LOW}%.\n"
                   f"Predicted Humidity: {predicted['predicted_humidity']}%\n\n"
                   f"Adjustments may be necessary. Please monitor the system.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: Low Predicted Humidity!", message)
        send_sms_alert(message)

    # Check actual pH level
    if actual['ph_level'] > PH_HIGH:
        message = (f"ALERT: High pH Level Detected!\n\n"
                   f"At {timestamp}, the pH level exceeded the safety limit of {PH_HIGH}.\n"
                   f"Current pH Level: {actual['ph_level']}\n\n"
                   f"Take corrective action to ensure proper nutrient absorption.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: High pH Level Alert!", message)
        send_sms_alert(message)
    elif actual['ph_level'] < PH_LOW:
        message = (f"ALERT: Low pH Level Detected!\n\n"
                   f"At {timestamp}, the pH level dropped below the safety limit of {PH_LOW}.\n"
                   f"Current pH Level: {actual['ph_level']}\n\n"
                   f"Correct the pH level to avoid plant stress.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Danger: Low pH Level Alert!", message)
        send_sms_alert(message)

    # Check predicted pH level
    if predicted['predicted_ph_level'] > PH_HIGH:
        message = (f"WARNING: High Predicted pH Level!\n\n"
                   f"At {timestamp}, the predicted pH level is expected to exceed the safety limit of {PH_HIGH}.\n"
                   f"Predicted pH Level: {predicted['predicted_ph_level']}\n\n"
                   f"Please monitor and take action if necessary.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: High Predicted pH Level!", message)
        send_sms_alert(message)
    elif predicted['predicted_ph_level'] < PH_LOW:
        message = (f"WARNING: Low Predicted pH Level!\n\n"
                   f"At {timestamp}, the predicted pH level is expected to drop below the safety limit of {PH_LOW}.\n"
                   f"Predicted pH Level: {predicted['predicted_ph_level']}\n\n"
                   f"Be prepared to adjust the pH level to ensure proper conditions.\n"
                   f"Best regards,\n{team_name}")
        send_email_alert("Warning: Low Predicted pH Level!", message)
        send_sms_alert(message)


# Real-time alert system loop (checking both actual and predicted data)
while True:
    # Fetch the most recent actual sensor data
    actual_data = fetch_latest_actual_data()

    # Fetch the most recent predicted data
    predicted_data = fetch_latest_predicted_data()

    if actual_data is not None and predicted_data is not None:
        # Check and trigger alerts based on actual and predicted data
        check_alerts(actual_data, predicted_data)

    # Wait for a while before making the next check (adjust the sleep time as needed)
    time.sleep(5)
