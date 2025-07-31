import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

# Kafka Consumer
consumer = KafkaConsumer(
    'taxi_trips',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='trip-db-writer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="taxi_data",
    user="taxi",
    password="taxi123",
    host="localhost",  # Docker exposes it to your host
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id SERIAL PRIMARY KEY,
        trip_id VARCHAR(20),
        pickup_location VARCHAR(50),
        drop_location VARCHAR(50),
        pickup_time TIMESTAMP,
        distance_km FLOAT,
        fare FLOAT,
        driver_id VARCHAR(20)
    );
""")
conn.commit()

print("📝 Listening for trips... Writing to PostgreSQL.")

# Process Kafka messages
for message in consumer:
    trip = message.value

    try:
        cursor.execute("""
            INSERT INTO trips (trip_id, pickup_location, drop_location, pickup_time, distance_km, fare, driver_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            trip["trip_id"],
            trip["pickup_location"],
            trip["drop_location"],
            datetime.fromisoformat(trip["pickup_time"]),
            trip["distance_km"],
            trip["fare"],
            trip["driver_id"]
        ))
        conn.commit()
        print(f"✅ Inserted trip {trip['trip_id']}")
    except Exception as e:
        print(f"❌ Failed to insert trip: {e}")
        conn.rollback()
