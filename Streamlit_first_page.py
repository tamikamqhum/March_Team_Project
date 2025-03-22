import streamlit as st
# Page Configurations
st.set_page_config(page_title="Pollution & Weather Insights",
                   page_icon="🌍",
                   layout="wide")

from app_pages.multi_page import MultiPage

# load pages scripts
# from streamlit.pollution_weather_analysis import pollution_weather_analysis
from multi_pages.forecast_aqi import forecast_aqi_page
from multi_pages.PG_Map_visualisation import map_visualisation_body
from multi_pages.PollutionCorrelationToWeather import correllation_body
from multi_pages.OvertimeMap import overtime_map_body
app = MultiPage(app_name= "Pollution and Weather Insights")  # Create an instance

# Add your app pages here using .add_page()
# app.add_page("Intro", pollution_weather_analysis)
app.add_page("Weather and Pollution", correllation_body)
app.add_page("Pollution Map", map_visualisation_body)
app.add_page("ML Forecast", forecast_aqi_page)
app.add_page("Overtime Map", overtime_map_body)

app.run() # Run the  app
