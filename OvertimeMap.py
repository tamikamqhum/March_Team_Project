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

theme = get_theme()
matplotlib.use("Agg")  # Use non-GUI backend to avoid font fallback spam

def overtime_map_body():
    # --- CONFIG ---
    DEFAULT_LOCATION = [38.456085, -92.288368]  # Center of continental US
    DEFAULT_ZOOM = 4

    # --- Load data ---
    df = pd.read_csv("Outputs//DashboardData.zip", parse_dates=["Date"])

    # Rename latitude and longitude columns
    df.rename(columns={"StationLatitude": "WS_Latitude", "StationLongitude": "WS_Longitude"}, inplace=True)

    # --- Weather indicators ---
    weather_vars = [
        "WT16", "WT01", "WT04", "WT18", "WT22", "WT09", "WT11", "WT06",
        "WT08", "WT05", "WT02", "WT13", "WT03",
        "TMAX", "TMIN", "TAVG", "TSUN", "AWND", "PGTM", "PRCP", "WDMV"
    ]

    # --- Weather icons and colors ---
    weather_icons = {
        "WT16": ("🌧️", "blue", "Rain"), "WT01": ("🌫️", "gray", "Fog"), "WT04": ("🌨️", "lightblue", "Sleet/Snow Pellets"),
        "WT18": ("❄️", "white", "Snow"), "WT22": ("🌫️", "gray", "Freezing Fog"), "WT09": ("🌬️", "lightgray", "Blowing Snow"),
        "WT11": ("💨", "orange", "High Winds"), "WT06": ("🧊", "cyan", "Glaze"), "WT08": ("🌫️", "darkgray", "Smoke/Haze"),
        "WT05": ("🌩️", "purple", "Hail"), "WT02": ("🌁", "lightgray", "Heavy Fog"), "WT13": ("🌁", "lightgray", "Mist"),
        "WT03": ("⛈️", "darkblue", "Thunderstorm")
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
        "Alabama": [32.806671, -86.791130], "Alaska": [61.370716, -152.404419],
        "Arizona": [33.729759, -111.431221], "Arkansas": [34.969704, -92.373123],
        "California": [36.116203, -119.681564], "Colorado": [39.059811, -105.311104],
        "Connecticut": [41.597782, -72.755371], "Delaware": [39.318523, -75.507141],
        "Florida": [27.766279, -81.686783], "Georgia": [33.040619, -83.643074],
        "Hawaii": [21.094318, -157.498337], "Idaho": [44.240459, -114.478828],
        "Illinois": [40.349457, -88.986137], "Indiana": [39.849426, -86.258278],
        "Iowa": [42.011539, -93.210526], "Kansas": [38.526600, -96.726486],
        "Kentucky": [37.668140, -84.670067], "Louisiana": [31.169546, -91.867805],
        "Maine": [44.693947, -69.381927], "Maryland": [39.063946, -76.802101],
        "Massachusetts": [42.230171, -71.530106], "Michigan": [43.326618, -84.536095],
        "Minnesota": [45.694454, -93.900192], "Mississippi": [32.741646, -89.678696],
        "Missouri": [38.456085, -92.288368], "Montana": [46.921925, -110.454353],
        "Nebraska": [41.125370, -98.268082], "Nevada": [38.313515, -117.055374],
        "New Hampshire": [43.452492, -71.563896], "New Jersey": [40.298904, -74.521011],
        "New Mexico": [34.840515, -106.248482], "New York": [42.165726, -74.948051],
        "North Carolina": [35.630066, -79.806419], "North Dakota": [47.528912, -99.784012],
        "Ohio": [40.388783, -82.764915], "Oklahoma": [35.565342, -96.928917],
        "Oregon": [44.572021, -122.070938], "Pennsylvania": [40.590752, -77.209755],
        "Rhode Island": [41.680893, -71.511780], "South Carolina": [33.856892, -80.945007],
        "South Dakota": [44.299782, -99.438828], "Tennessee": [35.747845, -86.692345],
        "Texas": [31.054487, -97.563461], "Utah": [40.150032, -111.862434],
        "Vermont": [44.045876, -72.710686], "Virginia": [37.769337, -78.169968],
        "Washington": [47.400902, -121.490494], "West Virginia": [38.491226, -80.954570],
        "Wisconsin": [44.268543, -89.616508], "Wyoming": [42.755966, -107.302490]
    }

    # --- Build map ---
    m = folium.Map(location=DEFAULT_LOCATION, zoom_start=DEFAULT_ZOOM)

    for _, row in grouped.iterrows():
        if display_level == "City":
            lat, lon = row["WS_Latitude"], row["WS_Longitude"]
        else:
            lat, lon = state_centroids.get(row["State"], DEFAULT_LOCATION)
        if pd.isna(lat) or pd.isna(lon):
            continue

        # Active WT types
        wt_active = [wt for wt in binary_vars if wt in row and row[wt] > 0]
        wt_display = "".join([weather_icons[wt][0] for wt in wt_active if wt in weather_icons])

        popup = f"<b>{row.get('City', row.get('State'))}</b><br>"
        label_map = {
            "TMAX": "Max Temp (°C)", "TMIN": "Min Temp (°C)", "TAVG": "Avg Temp (°C)",
            "TSUN": "Sunshine (min)", "AWND": "Avg Wind Speed (m/s)", "PGTM": "Peak Gust Time (HHMM)",
            "PRCP": "Precipitation (mm)", "WDMV": "Wind Movement (km)"
        }
        for var in numeric_vars:
            if pd.notna(row.get(var)):
                label = label_map.get(var, var)
                popup += f"{label}: {row[var]:.1f}<br>"
        if wt_display:
            popup += f"<b>Conditions:</b> {wt_display}"

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=popup
        ).add_to(m)

        # Add weather icons around marker with descriptive tooltips
        angle = 0
        for wt in wt_active:
            if wt in weather_icons:
                icon, color, desc = weather_icons[wt]
                offset_lat = lat + 0.3 * np.cos(np.radians(angle))
                offset_lon = lon + 0.3 * np.sin(np.radians(angle))
                folium.Marker(
                    location=[offset_lat, offset_lon],
                    icon=folium.DivIcon(html=f'<div style="font-size:18px">{icon}</div>'),
                    tooltip=desc
                ).add_to(m)
                angle += 360 / max(len(wt_active), 1)

    # --- Navigation Buttons ---
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_col1, date_col2, date_col3, date_col4, date, col1, col2, col3, col4 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1])
    with date_col4:
        st.write("")
        if st.button("⬅️ 1 Week"):
            st.session_state.date_choice = pd.Timestamp(max(min_date, st.session_state.date_choice.date() - timedelta(weeks=1)))
    with date_col3:
        st.write("")
        if st.button("⬅️ 1 Month"):
            st.session_state.date_choice = max(min_date, st.session_state.date_choice - timedelta(days=30))
    with date_col2:
        st.write("")
        if st.button("⬅️ 3 Months"):
            st.session_state.date_choice = max(min_date, st.session_state.date_choice - timedelta(days=90))
    with date_col1:
        st.write("")
        if st.button("⬅️ 1 Year"):
            st.session_state.date_choice = max(min_date, st.session_state.date_choice - timedelta(days=365))
    with col1:
        st.write("")
        if st.button("➡️ 1 Week"):
            st.session_state.date_choice = pd.Timestamp(min(max_date, st.session_state.date_choice.date() + timedelta(weeks=1)))
    with col2:
        st.write("")
        if st.button("➡️ 1 Month"):
            st.session_state.date_choice = min(pd.Timestamp(max_date), st.session_state.date_choice + timedelta(days=30))
    with col3:
        st.write("")
        if st.button("➡️ 3 Months"):
            st.session_state.date_choice = min(pd.Timestamp(max_date), st.session_state.date_choice + timedelta(days=90))
    with col4:
        st.write("")
        if st.button("➡️ 1 Year"):
            st.session_state.date_choice = min(pd.Timestamp(max_date), st.session_state.date_choice + timedelta(days=365))
    with date:
        # Date selector from calendar
        jump_date = st.date_input("Jump to Date", value=st.session_state.date_choice, min_value=min_date, max_value=max_date, key="jump")
        if jump_date != st.session_state.date_choice:
            st.session_state.date_choice = pd.Timestamp(jump_date)
    # --- Display map and legend ---
    left_col, right_col = st.columns([3, 1])

    with left_col:
        st_folium(m, width=1100, height=600)
        st.markdown("""
        ### Legend: WT Conditions
        Weather condition icons shown in popups:
        """)
        legend_cols = st.columns(4)
        icon_items = list(weather_icons.items())
        for i, (wt, (icon, color, desc)) in enumerate(icon_items):
            with legend_cols[i % 4]:
                st.markdown(f'<span style="color:{color}; font-size:20px">{icon}</span> {desc} ({wt})', unsafe_allow_html=True)

    with right_col:
        st.write("Display mode moved above")
        st.markdown("### 📅 Data Availability (daily record counts)")
        date_counts = df.groupby(df["Date"].dt.date).size()
        date_counts.index = pd.to_datetime(date_counts.index)
        date_counts.index.freq = None  # Let calplot infer spacing

        fig, axes = calplot(date_counts, cmap='Blues', colorbar=False)
        # Highlight selected date with a red dot
        highlight_date = pd.to_datetime(st.session_state.date_choice)
        if highlight_date in date_counts.index:
            for ax in np.ravel(axes):
                ax.plot(highlight_date, date_counts[highlight_date], 'ro', markersize=5)
        plt.tight_layout()
        st.pyplot(fig)
