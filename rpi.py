import requests
import time
import schedule
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

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
    elif response.status_code == 429:
        print("Rate limit exceeded. Waiting to retry...")
        time.sleep(60)  # Wait for 60 seconds before retrying
        return fetch_air_quality(city, state, country, api_key)  # Recursive retry
    elif response.status_code == 403:
        print("Access denied. Check your API key and permissions.")
        return None
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Function to send data to Firebase
def send_data_to_firebase(data):
    ref = db.reference('/air_quality_data')
    ref.push(data)

# Function to save data to a CSV file
def save_data_to_csv(data):
    with open('air_quality_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Define the headers for the CSV file based on the data structure
        file.seek(0, 2)  # Go to the end of the file
        if file.tell() == 0:  # Check if file is empty
            writer.writerow(['Timestamp', 'City', 'State', 'Country', 'AQI US', 'Main Pollutant US', 'Temperature', 'Humidity', 'Wind Speed', 'Wind Direction'])
        row = [
            data['data']['current']['pollution']['ts'],  # Timestamp for pollution data
            data['data']['city'],
            data['data']['state'],
            data['data']['country'],
            data['data']['current']['pollution']['aqius'],  # Air Quality Index US standard
            data['data']['current']['pollution']['mainus'],  # Main pollutant US standard
            data['data']['current']['weather']['tp'],  # Temperature
            data['data']['current']['weather']['hu'],  # Humidity
            data['data']['current']['weather']['ws'],  # Wind Speed
            data['data']['current']['weather']['wd']   # Wind Direction
        ]
        writer.writerow(row)

# Main function to run the data collection and ML analysis
def main():
    data = fetch_air_quality(city, state, country, api_key)
    if data:
        send_data_to_firebase(data)
        save_data_to_csv(data)
        print("Data sent to Firebase and saved to CSV successfully!")
        perform_ml_analysis()

# Perform ML analysis on updated CSV
def perform_ml_analysis():
    df = pd.read_csv('air_quality_data.csv')
    df = df.select_dtypes(include=[np.number]).dropna()  # Assuming 'AQI US' is numeric and we drop missing values
    X = df.drop('AQI US', axis=1)
    y = df['AQI US']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    plt.scatter(y_test, predictions)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.title('AQI Prediction')
    plt.show()

# Scheduler setup
schedule.every(12).seconds.do(main)

api_key = '0d0ad51f-d86a-445e-93a7-bf838bde20c4'
city = 'Los Angeles'
state = 'California'
country = 'USA'

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
