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

    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            mode = st.selectbox("Select Time Mode", ["Day", "Week", "Month", "Quarter", "Year"], index=2)

        with col2:
            if mode == "Day":
                selected_date = st.date_input("Select Date", df["Date"].min())
            elif mode == "Week":
                cola, colb = st.columns(2)
                with cola:
                    year = st.selectbox("Year", sorted(df["Date"].dt.year.unique(), reverse=True), key="week_year")
                with colb:
                    week = st.selectbox("Week", list(range(1, 54)))
                selected_date = pd.to_datetime(f"{year}-W{week}-1", format="%G-W%V-%u")
            elif mode == "Month":
                cola, colb = st.columns(2)
                with cola:
                    year = st.selectbox("Year", sorted(df["Date"].dt.year.unique(), reverse=True), key="month_year")
                with colb:
                    month = st.selectbox("Month", list(range(1, 13)))
                selected_date = pd.to_datetime(f"{year}-{month:02d}-01")
            else:
                selected_date = st.date_input("Select Date", df["Date"].min(), key="season_date")

        with col3:
            measure = st.selectbox("AQI Measure", ["NO2", "CO", "SO2", "O3"])

        with col4:
            display_level = st.selectbox("Display Level", ["City", "State"], index=1)

        with col5:
            show_weather = st.checkbox("Weather Icons", value=True)



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

    # Rename latitude and longitude columns
    df.rename(columns={"StationLatitude": "WS_Latitude", "StationLongitude": "WS_Longitude"}, inplace=True)

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

    if not df_filtered.empty:
        df_filtered = df_filtered.groupby(agg_level).agg(agg_dict).reset_index()

    # Create map
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

    def get_color(aqi_group):
        return {
            1: "#00e400", 2: "#a3ff00", 3: "#ffff00",
            4: "#ff7e00", 5: "#ff0000", 6: "#8f3f97"
        }.get(int(round(aqi_group)), "#808080")

    # Load geojson for US states
    geo_url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    geojson_data = requests.get(geo_url).json()
    df_filtered["Region"] = df_filtered["State"]

    # Choropleth
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

        # Remove default color bar
        for child in list(m._children):
            if child.startswith("color_map"):
                del m._children[child]
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
                popup=f"{row['City']}, {row['State']}<br>{measure} AQI Group: {round(row[f'{measure}_AQI_Group'], 2)}"
            ).add_to(m)

    # Weather icons
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

    # Render the map
    st_folium(m, width=1600, height=500)

    # Legend HTML block
    legend_html = f"""
    <div style="
        background-color: {theme['background']};
        border: 2px solid {theme['primary']};
        border-radius: 12px;
        padding: 15px;
        margin-top: 25px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        font-size: 15px;
        color: {theme['text']};
        font-family: 'sans-serif';
    ">
        <div style="font-weight: bold; font-size: 18px; margin-bottom: 12px; color: {theme['primary']};">
            Legend
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 30px; justify-content: flex-start;">
            <div style="flex: 1; min-width: 220px;">
                <div style="font-weight: bold; margin-bottom: 6px;">AQI Colors</div>
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <div><span style="background:#00e400; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Good (1)</div>
                    <div><span style="background:#a3ff00; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Moderate (2)</div>
                    <div><span style="background:#ffff00; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Unhealthy for Sensitive Groups (3)</div>
                    <div><span style="background:#ff7e00; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Unhealthy (4)</div>
                    <div><span style="background:#ff0000; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Very Unhealthy (5)</div>
                    <div><span style="background:#8f3f97; width:20px; height:20px; display:inline-block; border-radius:4px; margin-right:8px;"></span> Hazardous (6)</div>
                </div>
            </div>
            <div style="flex: 2; min-width: 300px;">
                <div style="font-weight: bold; margin-bottom: 6px;">Weather Icons</div>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
    """

    for code, icon in weather_icons.items():
        legend_html += f'<div style="min-width: 60px;"><span style="font-size:18px;">{icon}</span> <span style="font-size:13px;">{code}</span></div>'

    legend_html += f"""
                </div>
            </div>
        </div>
        <div style="margin-top: 12px; font-size: 13px; color: {theme['text']}cc;">
            <b>Note:</b> Areas shown in light red have no available data.
        </div>
    </div>
    """

    # Render the legend
    st.markdown(legend_html, unsafe_allow_html=True)
