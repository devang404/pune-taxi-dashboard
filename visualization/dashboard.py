import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from datetime import datetime
import base64


st.set_page_config(page_title="🚖 Pune Taxi Intelligence Dashboard", layout="wide")

# Business-modern UI enhancements
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f0f2f6, #dbe3ec);
    }
    .main .block-container {
        background-color: #ffffffcc;
        padding: 2.5rem 3rem;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.07);
    }
    .stMarkdown h1, h2, h3 {
        color: #2b2f77;
        font-family: 'Segoe UI', sans-serif;
    }
    .stMetricValue, .stMetricLabel {
        color: #004085 !important;
        font-weight: 600;
    }
    .css-1kyxreq {
        background: #f5f8fc;
        border-radius: 12px;
    }
    .stDataFrameContainer {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Load data from CSV instead of PostgreSQL for deployment
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv("visualization/trips.csv")
    df['pickup_time'] = pd.to_datetime(df['pickup_time'])
    df['hour'] = df['pickup_time'].dt.hour
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🎛️ Filters")
locations = sorted(df['pickup_location'].unique())
selected_location = st.sidebar.selectbox("Select Pickup Location", options=["All"] + locations)

start_date = st.sidebar.date_input("Start Date", value=df['pickup_time'].min().date())
end_date = st.sidebar.date_input("End Date", value=df['pickup_time'].max().date())
fare_max_threshold=df['fare'].quantile(0.95)

min_fare,max_fare=st.sidebar.slider(
    "Fare Range(Rupees)",
    min_value=60.0,
    max_value=float(fare_max_threshold),
    value=(60.0,float(fare_max_threshold)),
    step=1.0

)
# Show data coverage
st.sidebar.markdown("---")
st.sidebar.subheader("🕒 Data Coverage")
st.sidebar.write("Earliest:", df['pickup_time'].min())
st.sidebar.write("Latest:", df['pickup_time'].max())
st.sidebar.write(f"🚨 Raw data size: {df.shape[0]}")


# Filter 
filtered_df = df[
    (df['pickup_time'].dt.date >= start_date) &
    (df['pickup_time'].dt.date <= end_date) &
    (df['fare'] >= min_fare) & (df['fare'] <= max_fare)
]
if selected_location != "All":
    filtered_df = filtered_df[filtered_df['pickup_location'] == selected_location]

# Metrics
st.title("🚖 Pune Taxi Intelligence Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", len(filtered_df))
col2.metric("Total Revenue", f"₹{filtered_df['fare'].sum():,.2f}")
col3.metric("Avg Fare/km", f"₹{(filtered_df['fare'] / filtered_df['distance_km']).mean():.2f}")

# Charts
st.subheader("💰 Fare Distribution")
fig_fare = px.histogram(
    filtered_df,
    x='fare',
    nbins=15,
    title='Fare Distribution (₹)',
    color_discrete_sequence=['#8E24AA']
)
fig_fare.update_layout(
    xaxis_title='Fare (₹)',
    yaxis_title='Number of Trips',
    bargap=0.2,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig_fare, use_container_width=True)

st.subheader("📈 Trips by Hour")
hourly = filtered_df.groupby('hour').size().reset_index(name='trip_count')
fig_hour = px.line(hourly, x='hour', y='trip_count', title='Trips by Hour', markers=True, line_shape='linear', color_discrete_sequence=['#1E88E5'])
st.plotly_chart(fig_hour, use_container_width=True)


# Map
from folium.plugins import HeatMap, MarkerCluster

st.subheader("🗺️ Pickup Locations HeatMap + Pins")

location_coords = {
    "Swargate": (18.5018, 73.8615),
    "Hinjewadi": (18.5918, 73.7387),
    "Shivajinagar": (18.5308, 73.8470),
    "Koregaon Park": (18.5362, 73.8938),
    "Kothrud": (18.5089, 73.8077),
    "Wakad": (18.5990, 73.7682),
    "Baner": (18.5590, 73.7865),
    "Viman Nagar": (18.5679, 73.9143),
}

# Map setup
m = folium.Map(location=[18.5204, 73.8567], zoom_start=12)

# Heatmap data based on coordinates
heat_data = []
marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    coords = location_coords.get(row['pickup_location'])
    if coords:
        # Add to heatmap
        heat_data.append(coords)

        # Add marker to same location
        folium.Marker(
            location=coords,
            popup=folium.Popup(
                f"<b>Trip ID:</b> {row['trip_id']}<br><b>Fare:</b> ₹{row['fare']}<br><b>Driver:</b> {row['driver_id']}",
                max_width=250
            ),
            icon=folium.Icon(color='blue', icon='taxi', prefix='fa')
        ).add_to(marker_cluster)

# Add heatmap layer
HeatMap(heat_data, radius=18, blur=15, min_opacity=0.3, max_zoom=15).add_to(m)

# Render map
folium_static(m, width=1000, height=550)



# Live Trip Feed
st.subheader("📰 Latest Trips")
st.dataframe(filtered_df.sort_values(by='pickup_time', ascending=False).head(10))