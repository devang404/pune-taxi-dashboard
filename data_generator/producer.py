import json
import random
import time
from datetime import datetime,timedelta
from kafka import KafkaProducer
from faker import Faker

fake = Faker()

pune_locations = {
    "Swargate": (18.5018, 73.8615),
    "Hinjewadi": (18.5918, 73.7387),
    "Shivajinagar": (18.5308, 73.8470),
    "Koregaon Park": (18.5362, 73.8938),
    "Kothrud": (18.5089, 73.8077),
    "Wakad": (18.5990, 73.7682),
    "Baner": (18.5590, 73.7865),
    "Viman Nagar": (18.5679, 73.9143),
}

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_trip():
    pickup = random.choice(list(pune_locations.keys()))
    drop = random.choice([loc for loc in pune_locations if loc != pickup])
    distance = round(random.uniform(3, 15), 2)  # km
    fare = round(35 + (distance * random.uniform(10, 15)), 2)  # Rs
    return {
        "trip_id": f"TRIP-{random.randint(100000, 999999)}",
        "pickup_location": pickup,
        "drop_location": drop,
        "pickup_time": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),


        "distance_km": distance,
        "fare": fare,
        "driver_id": f"DR-{random.randint(1000, 9999)}"
    }

if __name__ == "__main__":
    for _ in range(275):  # generate 275trips quickly
        trip = generate_trip()
        producer.send("taxi_trips", trip)
        print(f"Produced: {trip}")
        time.sleep(0.01)  # 100 trips per second
