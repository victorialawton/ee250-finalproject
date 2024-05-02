import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK
cred = credentials.Certificate('airquality-7ed35-firebase-adminsdk-wfkbr-9a0fc8480e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://airquality-7ed35-default-rtdb.firebaseio.com/'
})

# Function to fetch air quality data
def fetch_air_quality(city, state, country, api_key):
    url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country={country}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Function to send data to Firebase
def send_data_to_firebase(data):
    ref = db.reference('/air_quality_data')
    ref.push(data)

# Replace these with your actual details
api_key = '0d0ad51f-d86a-445e-93a7-bf838bde20c4'
city = 'Los Angeles'
state = 'California'
country = 'USA'

# Fetch and send data
data = fetch_air_quality(city, state, country, api_key)
if data:
    send_data_to_firebase(data)
    print("Data sent to Firebase successfully!")
