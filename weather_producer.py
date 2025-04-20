import requests
import json
from kafka import KafkaProducer
import time
# OpenWeather API details
API_KEY = "fbf6087b5ea2cf2f8c19a7fc0e39c7bb"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# Kafka Producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# Function to fetch weather data
def get_weather_data(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params).json()
    return response
# Infinite loop for continuous data streaming
while True:
    city = "Chennai"
    weather_data = get_weather_data(city)
    if weather_data.get("cod") == 200:
        weather_info = {
            "city": city,
            "temperature": weather_data['main']['temp'],
            "humidity": weather_data['main']['humidity'],
            "weather": weather_data['weather'][0]['description'],
            "timestamp": weather_data['dt']
        }
        producer.send('weather_topic', value=weather_info)
        print(f"✅ Weather data sent: {weather_info}")
    else:
        print(f"❌ Failed to fetch data for {city}")
    time.sleep(30)  # Fetch data every 30 seconds