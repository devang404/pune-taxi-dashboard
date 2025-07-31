import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Connect using environment variables
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Query the data
df = pd.read_sql("SELECT * FROM trips ORDER BY pickup_time DESC LIMIT 1000", conn)

# Save to CSV
df.to_csv("D:/trips.csv", index=False)
print("✅ trips.csv saved to D drive successfully.")

