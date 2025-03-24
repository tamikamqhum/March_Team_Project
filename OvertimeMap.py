import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from calplot import calplot
from datetime import timedelta
from utils.theme import get_theme

# Apply theme settings
theme = get_theme()
matplotlib.use("Agg")  # Use non-GUI backend to avoid font fallback spam

def overtime_map_body():
    # --- CONFIG ---
    DEFAULT_LOCATION = [38.456085, -92.288368]  # Center of continental US
    DEFAULT_ZOOM = 4

    # --- Load data ---
    df = pd.read_csv("Outputs/DashBoardData.zip", parse_dates=["Date"])

    # Rename latitude and longitude columns
    df.rename(columns={"StationLatitude": "WS_Latitude", "StationLongitude": "WS_Longitude"}, inplace=True)

    # --- Weather indicators ---
    weather_vars = [
        "WT16", "WT01", "WT04", "WT18", "WT22", "WT09", "WT11", "WT06", "WT08", "WT05", 
        "WT02", "WT13", "WT03", "TMAX", "TMIN", "TAVG", "TSUN", "AWND", "PGTM", "PRCP", "WDMV"
    ]

    # --- Weather icons and colors ---
    weather_icons = {
        "WT16": ("🌧️", "blue", "Rain"),
        "WT01": ("🌫️", "gray", "Fog"),
        "WT04": ("🌨️", "lightblue", "Sleet/Snow Pellets"),
        "WT18": ("❄️", "white", "Snow"),
        "WT22": ("🌫️", "gray", "Freezing Fog"),
        "WT09": ("🌬️", "lightgray", "Blowing Snow"),
        "WT11": ("💨", "orange", "High Winds"),
        "WT06": ("🧊", "cyan", "Glaze"),
        "WT08": ("🌫️", "darkgray", "Smoke/Haze"),
        "WT05": ("🌩️", "purple", "Hail"),
        "WT02": ("🌁", "lightgray", "Heavy Fog"),
        "WT13": ("🌁", "lightgray", "Mist"),
        "WT03": ("⛈️", "darkblue", "Thunderstorm"),
    }

    # --- UI ---
    st.title("Weather Snapshot Map")
    st.markdown("### 🔎 Jump to Date")

    display_level = st.selectbox("Display Level", ["City", "State"], index=0)

    if "date_choice" not in st.session_state:
        st.session_state.date_choice = df["Date"].min()
    date_choice = st.session_state.date_choice

    # --- Filter Data ---
    filtered_df = df[df["Date"] == pd.to_datetime(date_choice)]

    if display_level == "City":
        group_cols = ["City", "State", "WS_Latitude", "WS_Longitude"]
    else:
        group_cols = ["State"]

    binary_vars = [col for col in weather_vars if col.startswith("WT")]
    numeric_vars = [col for col in weather_vars if col not in binary_vars]

    agg_dict = {col: "max" for col in binary_vars}
    agg_dict.update({col: "mean" for col in numeric_vars})

    grouped = filtered_df.groupby(group_cols).agg(agg_dict).reset_index()

    # --- State centroids ---
    state_centroids = {
        "Alabama": [32.806671, -86.791130], "Alaska": [61.370716, -152.404419], "Arizona": [33.729759, -111.431221],
        "Arkansas": [34.969704, -92.373123], "California": [36.116203, -119.681564], "Colorado": [39.059811, -105.311104],
        "Connecticut": [41.597782, -72.755371], "Delaware": [39.318523, -75.507141], "Florida": [27.766279, -81.686783],
        "Georgia": [33.040619, -83.643074], "Hawaii": [21.094318, -157.498337], "Idaho": [44.240459, -114.478828],
        "Illinois": [40.349457, -88.986137], "Indiana": [39.849426, -86.258278], "Iowa": [42.011539, -93.210526],
        "Kansas": [38.526600, -96.726486], "Kentucky": [37.668140, -84.670067], "Louisiana": [31.169546, -91.867805],
        "Maine": [44.693947, -69.381927], "Maryland": [39.063946, -76.802101], "Massachusetts": [42.230171, -71.530106],
        "Michigan": [43.326618, -84.536095], "Minnesota": [45.694454, -93.900192], "Mississippi": [32.741646, -89.678696],
        "Missouri": [38.456085, -92.288368], "Montana": [46.921925, -110.454353], "Nebraska": [41.125370, -98.268082],
        "Nevada": [38.313515, -117.055374], "New Hampshire": [43.452492, -71.563896], "New Jersey": [40.298904, -74.521011],
        "New Mexico": [34.840515, -106.248482], "New York": [42.165726, -74.948051], "North Carolina": [35.630066, -79.806419],
        "North Dakota": [47.528912, -99.784012], "Ohio": [40.388783, -82.764915], "Oklahoma": [35.565342, -96.928917],
        "Oregon": [44.572021, -122.070938], "Pennsylvania": [40.590752, -77.209755], "Rhode Island": [41.680893, -71.511780],
        "South Carolina": [33.856892, -80.945007], "South Dakota": [44.299782, -99.438828], "Tennessee": [35.747845, -86.692345],
        "Texas": [31.054487, -97.563461], "Utah": [40.150032, -111.862434], "Vermont": [44.045876, -72.710686],
        "Virginia": [37.769337, -78.169968], "Washington": [47.400902, -121.490494], "West Virginia": [38.491226, -80.954570],
        "Wisconsin": [44.268543, -89.616508], "Wyoming": [42.755966, -107.302490]
    }

    # --- Build map ---
    m = folium.Map(location=DEFAULT_LOCATION, zoom_start=DEFAULT_ZOOM)

    for _, row in grouped.iterrows():
        lat, lon = state_centroids.get(row["State"], DEFAULT_LOCATION) if display_level == "State" else (row["WS_Latitude"], row["WS_Longitude"])

        popup = f"<b>{row.get('City', row.get('State'))}</b><br>"
        for var in numeric_vars:
            if pd.notna(row.get(var)):
                popup += f"{var}: {row[var]:.1f}<br>"

        folium.CircleMarker(
            location=[lat, lon], radius=10, color="blue", fill=True, fill_color="blue", fill_opacity=0.6, popup=popup
        ).add_to(m)

    st_folium(m, width=1100, height=600)

overtime_map_body()