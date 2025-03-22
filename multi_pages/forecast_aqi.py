import streamlit as st
import pandas as pd
from app_pages.aqi_model_utils import prepare_input, predict_aqi_group, get_model_metadata, FEATURES
from datetime import datetime
import matplotlib.pyplot as plt

def forecast_aqi_page():
    st.markdown("---")
    st.title("Forecast AQI Group")
    st.markdown("---")
    st.markdown("Use this tool to predict AQI groups using weather conditions and date.")
    col1, col2 = st.columns([1, 1])
    with col1:
        target = st.selectbox("Select AQI Group to Predict", [
            "O3_AQI_Group", "SO2_AQI_Group", "CO_AQI_Group", "NO2_AQI_Group"
        ])
    with col2:
        date_input = st.date_input("Select Date", value=datetime.today())
    st.markdown("---")

    weather_data = {}

    # === Temperature Group ===
    st.subheader("🌡️ Temperature")
    cols = st.columns(3)
    weather_data["TAVG"] = cols[0].number_input("Avg Temperature (°C)", value=20.0)
    weather_data["TMAX"] = cols[1].number_input("Max Temperature (°C)", value=25.0)
    weather_data["TMIN"] = cols[2].number_input("Min Temperature (°C)", value=15.0)
    st.markdown("---")
    # === Precipitation Group ===
    st.subheader("🌧️ Precipitation")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    weather_data["PRCP"] = col1.number_input("Precipitation (mm)", value=0.0)
    with col2:
        st.markdown("**Precipitation Conditions:**")
        wt_precip_flags = {
            "Freezing Rain (WT01)": st.checkbox("Freezing Rain", key="WT01"),
            "Thunderstorms (WT08)": st.checkbox("Thunderstorms", key="WT08"),
        }
    with col3:
        wt_precip_flags2 = {
            "Rain (WT14)": st.checkbox("Rain", key="WT14"),
            "Drizzle (WT11)": st.checkbox("Drizzle", key="WT11"),
        }
    with col4:
        wt_precip_flags3 = {
            "Blowing Snow (WT09)": st.checkbox("Blowing Snow", key="WT09"),
            "Snow (WT15)": st.checkbox("Snow", key="WT15"),
            "Ice Pellets (WT17)": st.checkbox("Ice Pellets", key="WT17"),
        }
        
        wt_precip_flags.update(wt_precip_flags2)
        wt_precip_flags.update(wt_precip_flags3)
        weather_data["WT_Precip"] = sum(int(val) for val in wt_precip_flags.values())
    st.markdown("---")
    # === Wind Group ===
    st.subheader("💨 Wind")
    col1, col2 = st.columns([2, 3])
    weather_data["AWND"] = col1.number_input("Avg Wind Speed (m/s)", value=5.0)
    weather_data["WDMV"] = col1.number_input("Fastest Wind Speed (m/s)", value=8.0)
    with col2:
        st.markdown("**Wind Conditions:**")
        wt_wind_flags = {
            "High Winds (WT06)": st.checkbox("High Winds", key="WT06"),
            "Wind Damage (WT13)": st.checkbox("Wind Damage", key="WT13"),
        }
        weather_data["WT_Wind"] = sum(int(val) for val in wt_wind_flags.values())
    st.markdown("---")
    # === Extreme Weather Group ===
    st.subheader("⚡ Extreme / Other Weather")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        st.markdown("**Extreme Events:**")
        wt_extreme_flags = {
            "Hail (WT18)": st.checkbox("Hail", key="WT18"),
            "Tornado (WT22)": st.checkbox("Tornado", key="WT22"),
        }
        weather_data["WT_Extreme"] = sum(int(val) for val in wt_extreme_flags.values())
    with col2:
        st.markdown("**Other Weather Types:**")
        wt_other_flags = {
            "Freezing Rain (WT01)": st.checkbox("Freezing Rain", key="WT01b"),
            "Fog (WT02)": st.checkbox("Fog Again?", key="WT02_alt"),  
        }
    with col3:
        wt_other_flags2 = {
            "Blowing Snow (WT03)": st.checkbox("Blowing Snow", key="WT03"),
            "Dust Storm (WT04)": st.checkbox("Dust Storm", key="WT04"),
        }
    with col4:
        wt_other_flags3 = {
            "Sleet (WT05)": st.checkbox("Sleet", key="WT05"),
            "Snow Pellets (WT16)": st.checkbox("Snow Pellets", key="WT16"),
        }
        # combine wt_other_flags
        wt_other_flags.update(wt_other_flags2)
        wt_other_flags.update(wt_other_flags3)
        weather_data["WT_Other"] = sum(int(val) for val in wt_other_flags.values())
    st.markdown("---")
    # === Location Group ===
    st.subheader("📍 Location")
    st.markdown("*Only valid for cities within the continental USA*")

    # Load city location data (must be present in app directory as 'Us_Stations.csv')
    
    col1, col2, col3 = st.columns([1, 1, 1])
    @st.cache_data
    def load_city_locations():
        df = pd.read_csv("Source_Data//Us_Stations_with_City_100km.csv", usecols=["City", "Name", "Latitude", "Longitude"])
        df["City"] = df["City"].str.lower()
        return df

    cities_df = load_city_locations()
    with col1:
        city_input = st.text_input("Enter Closest City Name").strip().lower()

    lat, lon = None, None
    if city_input:
        matches = cities_df[cities_df["City"] == city_input]
        if not matches.empty:
            city_row = matches.iloc[0]
            lat = city_row["Latitude"]
            lon = city_row["Longitude"]
            st.success(f"Found location: {city_row['City'].title()}, {city_row['Name']} (Lat: {lat}, Lon: {lon})")
        else:
            st.warning("City not found. Please check spelling or try a nearby city.")

    # Show resolved lat/lon
    weather_data["WS_Latitude"] = lat if lat is not None else 0.0
    weather_data["WS_Longitude"] = lon if lon is not None else 0.0
    with col2:
        weather_data["CityDistance"] = st.number_input("Distance to Nearest City (km)", value=10.0)
    with col3:
        weather_data["WS_Elevation"] = st.number_input("Station Elevation (m)", value=200.0)

    st.markdown("---")

    # === Predict & Explain ===
    if st.button("Predict"):
        input_df = prepare_input(date_input, weather_data)
        result = predict_aqi_group(target, input_df)
        st.success(f"Predicted AQI Group for {target}: **{result}**")
        # translate AQI group to description
        def AQI_Range(value):
            if value == 1:
                return 'Good'
            if value == 2:
                return 'Moderate'
            if value == 3:
                return 'Unhealthy for Sensitive Groups'
            if value == 4:
                return 'Unhealthy'
            if value == 5:
                return 'Very Unhealthy'
            if value == 6:
                return 'Hazardous'
            return 'Unknown'

        def AQI_Range_Description(value):
            if value == 1:
                return 'Air quality is considered satisfactory, and air pollution poses little or no risk.'
            if value == 2:
                return 'Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.'
            if value == 3:
                return 'Members of sensitive groups may experience health effects. The general public is not likely to be affected.'
            if value == 4:
                return 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.'
            if value == 5:
                return 'Health alert: everyone may experience more serious health effects.'
            if value == 6:
                return 'Health warnings of emergency conditions. The entire population is more likely to be affected.'
            return 'Unknown'

        def AQI_Range_Value(value):
            if value == 1:
                return "0-50"
            if value == 2:
                return "51-100"
            if value == 3:
                return "101-150"
            if value == 4:
                return "151-200"
            if value == 5:
                return "201-300"
            if value == 6:
                return "301-500"
            return 'Unknown'

        # The model returns a number from 1 to 6, which corresponds to the AQI group
        # The AQI group is then translated to a range and description
        
        aqi_range_value = AQI_Range_Value(result)
        aqi_range = AQI_Range(result)
        aqi_range_description = AQI_Range_Description(result)
        st.markdown(f"**AQI Group:** {aqi_range} ({aqi_range_value})")
        st.markdown(f"**Description:** {aqi_range_description}")        
        
            
            
        metadata = get_model_metadata(target)
        if metadata:
            st.subheader("Feature Importances")
            importances = metadata["feature_importances"]
            fig, ax = plt.subplots()
            ax.barh(list(importances.keys()), list(importances.values()))
            ax.set_xlabel("Importance")
            ax.set_title(f"{target} Feature Importances")
            st.pyplot(fig)

            st.markdown(f"**AQI Classes:** {', '.join(map(str, metadata['classes']))}")

    st.markdown("---")
    st.markdown("🔍 **Feature Descriptions**")
    st.write(FEATURES)

    st.markdown("---")
    st.markdown("📚 **Data Sources**")
    st.markdown("1. [NOAA Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/)")
    st.markdown("2. [US EPA Air Quality Data](https://www.epa.gov/outdoor-air-quality-data)")
    st.markdown("3. [National Weather Service](https://www.weather.gov/)")

    st.markdown("---")
    st.markdown("🔗 **Project Repository**")
    st.markdown("View the source code and contribute on [GitHub](https://github.com/Hysnap/March_Team_Project)")

    st.markdown("---")
    