import streamlit as st
<<<<<<< HEAD:streamlit/pollution_weather_analysis.py
<<<<<<< HEAD
=======
from utils.theme import get_theme
>>>>>>> 8dd9f8210c7c13c197c17dc15e2f80411222278f:pollution_weather_analysis.py

theme = get_theme()

def Intro():
    # Intro Section 
    st.title("🌍 Pollution & Weather Insights (2000-2016)")
    st.markdown("""
    Welcome to our interactive platform! This app explores **pollution trends** across the United States and their **relationship with weather patterns**. 

    🧐 **What you’ll discover:**
    - Fascinating trends in air pollution and climate.
    - Insights backed by statistical analysis and visualizations.
    - Tools to filter data by location and time period.

    💡 **How to navigate:**
    - Use the sidebar to explore visualizations, interactive maps, and summaries.
    - Dive into actionable insights for policymakers and environmentalists.

    ---
    """)

    # Add button 
    if st.button("Get Started 👉"):
        st.write("Head to sidebar to begin exploring!")


    # Explanation Section 
    st.title("🔍Overview")
    st.markdown("""
    This project is a comprehensive analysis of **pollution** and **weather data** from **2000 to 2016**.

    ## Why This Matters
    Air pollution and weather patterns are crucial to understanding the environmental challenges we face. By analyzing this data, we aim to provide insights into:
    - Long-term trends in air quality.
    - How weather impacts pollution levels.
    - Data-driven recommendations for better policies.

    ## Key Features of the Dashboard
    - 📈 **Trends Analysis:** Time-series graphs to track pollution changes.
    - 🌍 **Geographic Insights:** Heatmaps and interactive maps.
    - ⚡ **Actionable Insights:** Hypothesis validation for better understanding.

    ## How We Did This
    Our approach combines data science, visual storytelling, and interactive technology:
    - Cleaned and analyzed datasets from trusted sources.
    - Conducted correlation checks and predictive modeling.
    - Designed with Streamlit for an engaging user experience.

    ## Ethical Considerations
    We are committed to responsible data use:
    - Transparency in our analysis.
    - Privacy for all datasets involved.
    - Promoting environmental awareness.

    ---
    """)
=======
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import joblib
import matplotlib.pyplot as plt
import numpy as np
import zipfile
import os


# 🚀 **Page Configurations**
st.set_page_config(page_title="Pollution & Weather Insights", page_icon="🌍", layout="wide")


# **Define ZIP file path & Model Path**
zip_path = r"C:\Users\tmqhu\Documents\March_Team_Project\Outputs\DashBoardData.zip"
model_path = r"C:\Users\tmqhu\Documents\March_Team_Project\Outputs\CO_AQI_Model.pkl"
scaler_path = r"C:\Users\tmqhu\Documents\March_Team_Project\Outputs\Scaler.pkl"


# 🚀 **Extract and Load Data**
@st.cache_data
def load_data():
    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open("DashBoardData") as file:  
            df = pd.read_csv(file, low_memory=False)
   
    # 🚀 **Convert 'Date' column properly**
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Handle conversion errors safely
    df["Date"] = df["Date"].dt.date  # Store as date only to prevent Arrow errors
    return df


data = load_data()


# 🚀 **Fix: Sidebar Navigation**
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Predictions", "Insights"])


# **🏠 Home Page**
if page == "Home":
    st.title("🌍 Pollution & Weather Insights (2000-2016)")
   
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Welcome to our interactive dashboard! Explore **pollution trends** and their **relationship with weather**.


        ### 🔍 What You Can Do Here:
        - Analyze pollution trends over time.
        - Check how weather impacts air quality.
        - Predict AQI levels using machine learning models.


        ### 📊 Key Features:
        - **Interactive graphs & maps** 📈
        - **Custom filters for locations & dates** 📅
        - **Machine learning predictions** 🤖
        """)


    with col2:
        st.image("https://cms.accuweather.com/wp-content/uploads/2020/02/cropped-city-under-a-cloudy-sky-2771744.jpg",
                 use_column_width=True)


    st.markdown("---")
   
    if st.button("Get Started 👉"):
        st.sidebar.info("Use the sidebar to navigate through the dashboard.")


# **📊 Data Exploration Page**
elif page == "Data Exploration":
    st.title("📊 Data Exploration")
   
    tab1, tab2 = st.tabs(["Trends", "Summary Statistics"])
   
    with tab1:
        pollutant = st.selectbox("Select Pollutant", ["CO AQI", "O3 AQI", "PM2.5 AQI", "NO2 AQI"])


        start_date, end_date = st.slider(
            "Select Date Range",
            min_value=data["Date"].min(),
            max_value=data["Date"].max(),
            value=(data["Date"].min(), data["Date"].max())
        )


        filtered_data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]


        # 🚀 **Line Chart**
        fig = px.line(filtered_data, x="Date", y=pollutant, title=f"{pollutant} Trends Over Time",
                      line_shape="linear", color_discrete_sequence=["#5ab2eb"])
        st.plotly_chart(fig, use_container_width=True)


        # 🚀 **Heatmap**
        st.subheader("Pollution Heatmap")
        heatmap_fig = px.density_heatmap(filtered_data, x="Date", y=pollutant, z=pollutant,
                                         color_continuous_scale=["#d9534f", "#63d463"])
        st.plotly_chart(heatmap_fig, use_container_width=True)


    with tab2:
        st.subheader("📌 Summary Statistics")
        st.write(filtered_data.describe())


# **🤖 Prediction Page**
elif page == "Predictions":
    st.title("🤖 Machine Learning Predictions")


    col1, col2 = st.columns([1, 1])
   
    with col1:
        st.markdown("### Input Weather Conditions")
        temp = st.number_input("Temperature (°C)", min_value=-10, max_value=50, value=20)
        humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=50)
        windspeed = st.slider("Wind Speed (m/s)", min_value=0, max_value=15, value=5)


    with col2:
        st.markdown("### Predicted AQI Level")


        # 🚀 **Check if model files exist before loading**
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            st.error("🚨 Model files not found! Please check the path.")
        else:
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)


            # 🚀 **Ensure input data is properly formatted**
            input_data = np.array([[temp, humidity, windspeed]])  # Convert to NumPy array
            input_data_scaled = scaler.transform(input_data)  # Scale input
            prediction = model.predict(input_data_scaled)[0]


            st.metric(label="Predicted CO AQI", value=round(prediction, 2))


# **📌 Insights Page**
elif page == "Insights":
    st.title("📌 Key Insights & Recommendations")
   
    tab1, tab2 = st.tabs(["🔬 Findings", "📢 Policy Recommendations"])
   
    with tab1:
        st.markdown("""
        ### 🔬 Key Findings
        - 🌡️ **Higher temperatures** correlate with **increased CO levels**.
        - 🏙️ **Urban areas** show **higher pollution** than rural areas.
        - 💨 **Wind speed helps reduce** pollution concentration.
        """)


    with tab2:
        st.markdown("""
        ### 📢 Policy Recommendations
        - 🏭 **Improve urban air monitoring** to track pollution hotspots.
        - 🌞 **Implement pollution control measures** in high-temperature seasons.
        - 🚦 **Promote policies encouraging reduced emissions** in high-risk zones.
        """)


st.sidebar.markdown("---")
st.sidebar.write("📌 **Developed for Environmental Analysis**")
>>>>>>> 60d6e34 (Merged update)
