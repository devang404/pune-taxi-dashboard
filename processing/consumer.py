import json
import csv
import os
from kafka import KafkaConsumer
from datetime import datetime

# Ensure directory exists
os.makedirs("visualization", exist_ok=True)

# Kafka consumer config
consumer = KafkaConsumer(
    'taxi_trips',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='trip-dashboard-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# CSV file setup
csv_file = "visualization/trips.csv"
file_exists = os.path.isfile(csv_file)

# Ensure header if creating new file
with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'trip_id', 'pickup_location', 'drop_location', 'pickup_time',
        'distance_km', 'fare', 'driver_id'
    ])
    if not file_exists:
        writer.writeheader()

print("🚕 Kafka Consumer started. Listening for taxi trip data...")

# Process incoming messages
for message in consumer:
    trip = message.value

    # Append to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=trip.keys())
        writer.writerow(trip)

    print(f"✅ Trip added: {trip['trip_id']} from {trip['pickup_location']} to {trip['drop_location']} | Fare ₹{trip['fare']}")