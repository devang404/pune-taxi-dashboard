

# 🚖 Pune Taxi Intelligence Dashboard

An interactive, real-time dashboard to analyze and visualize taxi trip data across Pune. Built using **Streamlit**, **Kafka**, **Folium**, and **PostgreSQL**, this project simulates and displays city-wide ride analytics with heatmaps, marker pins, and detailed metrics.

---

## 📊 Features

- **Real-time Kafka pipeline** for simulating and consuming taxi trip data
- **Interactive dashboard** with filters (date, fare, location)
- **Heatmap & Marker Pin toggle** to view high-traffic zones
- **Dynamic charts**: fare distribution and hourly trip trends
- **Live trip feed** & trip stats by location
- **CSV export** and persistent storage

---

## 🛠️ Tech Stack

| Tool         | Description                                   |
|--------------|-----------------------------------------------|
| Streamlit    | UI & dashboard rendering                      |
| Kafka        | Real-time data pipeline (Producer + Consumer) |
| Folium       | Interactive maps and heatmaps                 |
| PostgreSQL   | Optional persistent backend (via Docker)      |
| Docker       | Containerized local development               |
| pandas       | Data handling and transformation              |

---

## ⚙️ Project Structure

```bash
pune-taxi-dashboard/
│
├── visualization/            # Streamlit App (main dashboard)
│   ├── dashboard.py         # Streamlit logic
│   ├── trips.csv            # Main CSV data file
│
|___data_generator/
|    |__producer.py            #Kafka producer generating taxi trip data
|    
├── processing/
│   ├── db_writer.py          # (Optional)Writes data to PostgreSQL
│   ├── consumer.py          # Kafka consumer to write to CSV
│
├── docker/
│   ├── docker-compose.yml   # Kafka + Zookeeper + PostgreSQL setup
|
|__export_to_csv.py         #Exports data from PostgreSQL to trips.csv
|
├── .streamlit/
│   └── config.toml          #Streamlit app layout and theme
├── requirements.txt         # Dependencies for the app
├── README.md




##🚀 How to Run Locally

1️⃣ Clone the Repository

```bash
  git clone https://github.com/devang404/pune-taxi-dashboard.git
  cd pune-taxi-dashboard
```

2️⃣ Start Kafka + Zookeeper + PostgreSQL

```bash
  cd docker
  docker-compose up -d
```

3️⃣ Start Kafka Producer & Consumer

```bash
  #Terminal 1
  python processing/producer.py

  # Terminal 2
  python processing/consumer.py
```

4️⃣ Launch the Streamlit Dashboard

```bash
  streamlit run app/dashboard.py
```


## Deployment



```bash
1.Push your repo to GitHub.
2.Go to Streamlit Cloud and create a new app:
    2.1. Repository: devang404/pune-taxi-dashboard
    2.2. Branch:main
    2.3. Main file: visualization/dashboard.py

3.Add a trips.csv file with sample or exported data so Streamlit can display the dashboard without Kafka.

4.Add any secrets if required (like Supabase/DB keys) via Streamlit’s "Secrets" tab.
```


