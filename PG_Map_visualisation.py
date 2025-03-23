import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import json
import requests
import numpy as np
from utils.theme import get_theme

theme = get_theme()


def map_visualisation_body():
    # Load data from ZIP using pandas (single file in zip assumption)
    df = pd.read_csv("Outputs/DashBoardData.zip", parse_dates=["Date"])

    # Streamlit UI
    st.title("Air Quality Map with Filters")

    # Sidebar filters
    mode = st.sidebar.selectbox("Select Time Mode", ["Day", "Week", "Month", "Quarter", "Year"])
    if mode == "Day":
        selected_date = st.sidebar.date_input("Select Date", df["Date"].min())
    elif mode == "Week":
        year = st.sidebar.selectbox("Select Year", sorted(df["Date"].dt.year.unique(), reverse=True))
        week = st.sidebar.selectbox("Select Week", list(range(1, 54)))
        selected_date = pd.to_datetime(f"{year}-W{week}-1", format="%G-W%V-%u")
    elif mode == "Month":
        year = st.sidebar.selectbox("Select Year", sorted(df["Date"].dt.year.unique(), reverse=True))
        month = st.sidebar.selectbox("Select Month", list(range(1, 13)))
        selected_date = pd.to_datetime(f"{year}-{month:02d}-01")
    else:
        selected_date = st.sidebar.date_input("Select Date", df["Date"].min())
    measure = st.sidebar.selectbox("Select AQI Measure", ["NO2", "CO", "SO2", "O3"])
    show_weather = st.sidebar.checkbox("Show Weather Icons Around Markers", value=True)
    display_level = st.sidebar.selectbox("Display Level", ["City", "State"])

    # Weather condition mapping
    weather_icons = {
        "WT01": "🌫️", "WT02": "🌁", "WT03": "⛈️", "WT04": "🌨️", "WT05": "🌩️",
        "WT06": "🧊", "WT08": "🌫️", "WT09": "🌬️", "WT11": "💨", "WT13": "🌁",
        "WT16": "🌧️", "WT18": "❄️", "WT22": "🌫️"
    }

    # Convert to datetime
    selected_date = pd.to_datetime(selected_date)

    # Add Season column
    df['Season'] = df['Date'].dt.month % 12 // 3 + 1
    season_map = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Autumn'}
    df['SeasonGroup'] = df['Season'].map(season_map)

    # Define aggregation level
    agg_level = {
        "City": ["City", "State", "WS_Latitude", "WS_Longitude"],
        "State": ["State"]
    }[display_level]

    weather_cols = list(weather_icons.keys())
    agg_dict = {f"{measure}_AQI_Group": "mean"}
    agg_dict.update({col: "max" for col in weather_cols})

    # Filter and aggregate by selected mode
    if mode == "Day":
        df_filtered = df[df["Date"] == selected_date]
    elif mode == "Week":
        week = selected_date.isocalendar().week
        year = selected_date.year
        df_filtered = df[df["Date"].dt.isocalendar().week == week]
        df_filtered = df_filtered[df_filtered["Date"].dt.year == year]
    elif mode == "Month":
        df_filtered = df[(df["Date"].dt.month == selected_date.month) & (df["Date"].dt.year == selected_date.year)]
    elif mode == "Quarter":
        quarter = (selected_date.month - 1) // 3 + 1
        df_filtered = df[df["Date"].dt.to_period("Q") == f"{selected_date.year}Q{quarter}"]
    elif mode == "Year":
        df_filtered = df[df["Date"].dt.year == selected_date.year]
    else:
        df_filtered = df[df["SeasonGroup"] == df[df["Date"] == selected_date]["SeasonGroup"].iloc[0]]

    # Group by level
    if not df_filtered.empty:
        df_filtered = df_filtered.groupby(agg_level).agg(agg_dict).reset_index()

    # Create map and city polygons if City level
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    # Color map for AQI levels
    def get_color(aqi_group):
        return {
            1: "#00e400", 2: "#a3ff00", 3: "#ffff00",
            4: "#ff7e00", 5: "#ff0000", 6: "#8f3f97"
        }.get(int(round(aqi_group)), "#808080")

    # Load geojson for US states
    geo_url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    geojson_data = requests.get(geo_url).json()

    # Add region key
    df_filtered["Region"] = df_filtered["State"]

    # Add choropleth layer
    if display_level == "State":
        choropleth = folium.Choropleth(
            geo_data=geojson_data,
            name="choropleth",
            data=df_filtered,
            columns=["Region", f"{measure}_AQI_Group"],
            key_on="feature.properties.name",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            nan_fill_color="#ffcccc",
            nan_fill_opacity=0.3,
            legend_name=f"{measure} AQI Group"
        )
        choropleth.add_to(m)
    else:
        for _, row in df_filtered.iterrows():
            lat = row.get("WS_Latitude")
            lon = row.get("WS_Longitude")
            if pd.isna(lat) or pd.isna(lon):
                continue
            color = get_color(row[f"{measure}_AQI_Group"])
            folium.Circle(
                location=[lat, lon],
                radius=10000,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=f"{row['City']}, {row['State']}<br>{measure} AQI Group: {round(row[f'{measure}_AQI_Group'], 2)}").add_to(m)

    # Add weather icons if enabled
    if show_weather:
        city_weather = df[df["Date"].dt.to_period(mode[0]) == selected_date.to_period(mode[0])]
        city_weather = city_weather.groupby(["City", "State", "WS_Latitude", "WS_Longitude"])[weather_cols].max().reset_index()
        for _, row in city_weather.iterrows():
            lat, lon = row["WS_Latitude"], row["WS_Longitude"]
            if pd.isna(lat) or pd.isna(lon):
                continue
            conditions = [col for col in weather_cols if col in row and row[col] == 1]
            angle = 0
            for condition in conditions:
                offset_lat = lat + 0.1 * np.cos(np.radians(angle))
                offset_lon = lon + 0.1 * np.sin(np.radians(angle))
                folium.Marker(
                    location=[offset_lat, offset_lon],
                    popup=condition,
                    icon=folium.DivIcon(html=f'<div style="font-size:18px">{weather_icons[condition]}</div>')
                ).add_to(m)
                angle += 360 / max(len(conditions), 1)

    # Optional: show bar charts for AQI values at each city
    if display_level == "City" and st.sidebar.checkbox("Show AQI Bar Charts"):
        for _, row in df_filtered.iterrows():
            lat = row.get("WS_Latitude")
            lon = row.get("WS_Longitude")
            if pd.isna(lat) or pd.isna(lon):
                continue
            aqi_values = []
            labels = []
            colors = []
            for pollutant in ["NO2", "CO", "SO2", "O3"]:
                value = row.get(f"{pollutant}_AQI_Group")
                if not pd.isna(value):
                    aqi_values.append(value)
                    labels.append(pollutant)
                    colors.append(get_color(value))
            if aqi_values:
                html = '<div style="width:120px; height:100px;">'
                for label, val, color in zip(labels, aqi_values, colors):
                    html += f'<div style="background:{color};width:{int(val*15)}px">{label}: {val}</div>'
                html += '</div>'
                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(html=html)
                ).add_to(m)
    legend_html = '''
    <div style="position: fixed; 
        top: 80px; right: 20px; width: 260px; height: auto; 
        background-color: white; border:2px solid grey; z-index:9999; font-size:14px; padding: 10px">
    <b>Legend</b><br>
    <b>AQI Colors:</b><br>
    <i style="background:#00e400">&nbsp;&nbsp;&nbsp;&nbsp;</i> Good (1)<br>
    <i style="background:#a3ff00">&nbsp;&nbsp;&nbsp;&nbsp;</i> Moderate (2)<br>
    <i style="background:#ffff00">&nbsp;&nbsp;&nbsp;&nbsp;</i> Unhealthy for Sensitive Groups (3)<br>
    <i style="background:#ff7e00">&nbsp;&nbsp;&nbsp;&nbsp;</i> Unhealthy (4)<br>
    <i style="background:#ff0000">&nbsp;&nbsp;&nbsp;&nbsp;</i> Very Unhealthy (5)<br>
    <i style="background:#8f3f97">&nbsp;&nbsp;&nbsp;&nbsp;</i> Hazardous (6)<br>
    <br><b>Weather Icons:</b><br>
    ''' + ''.join([f'{icon} - {code}<br>' for code, icon in weather_icons.items()]) + '<br><b>Note:</b> Areas shown in light red have no available data.</div>'
    m.get_root().html.add_child(folium.Element(legend_html))

    # Render map in Streamlit
    st_folium(m, width=1600, height=500)
