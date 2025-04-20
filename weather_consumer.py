from kafka import KafkaConsumer
import json
import pandas as pd
import os

# Kafka Consumer setup
consumer = KafkaConsumer(
    'weather_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='weather-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# CSV file to store weather data
csv_file = "weather_data.csv"

# Check if the CSV file exists; if not, create it with headers
if not os.path.exists(csv_file):
    pd.DataFrame(columns=["city", "temperature", "humidity", "weather", "timestamp"]).to_csv(csv_file, index=False)

# Process incoming weather data
for message in consumer:
    weather = message.value
    # Convert the weather data to a DataFrame
    df = pd.DataFrame([weather])
    # Append the data to the CSV file
    df.to_csv(csv_file, mode='a', header=False, index=False)
    print(f"✅ Weather data appended to {csv_file}: {weather}")