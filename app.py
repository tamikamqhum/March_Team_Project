# app.py
import streamlit as st
import toml
# 🎛️ Page Config
st.set_page_config(page_title="Pollution & Weather Insights",
                   page_icon="🌍",
                   layout="wide")
try:
    from streamlit_option_menu import option_menu

    # 🧠 Page Imports
    from pollution_weather_analysis import Intro
    from JupyterNotebook import jupyter_notebook_viewer
    from PollutionCorrelationToWeather import pollution_weather_analysis
    from PG_Map_visualisation import map_visualisation_body
    from OvertimeMap import overtime_map_body
    from forecast_aqi import forecast_aqi_page
    from PollutionCorrelationToWeather_v1 import correllation_body2
except ImportError as e:
    st.error(f"An import error occurred: {e}")

# Load config from .streamlit/config.toml
config = toml.load(".streamlit/config.toml")
theme = config.get("theme", {})

primary = theme.get("primaryColor", "#5ab2e6")
secondary_bg = theme.get("secondaryBackgroundColor", "#63d463")
text = theme.get("textColor", "#0a0a0a")


# 🎨 Sidebar Menu
with st.sidebar:
    selected_page = option_menu(
        "Navigation",
        ["Intro",
         "Correlation",
         "More Correlations",
         "Pollution Map",
         "Weather Map",
         "ML Forecast",
         "Notebook"],
        icons=["house",
               "calculator",
               "bar-chart",
               "map",
               "cloud",
               "activity",
               "book"],
        menu_icon="menu-app",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": secondary_bg},
            "icon": {"color": text, "font-size": "18px"},
            "nav-link": {"color": text, "font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": primary, "color": "white"},
        }
    )

# 🔀 Page Routing
if selected_page == "Intro":
    Intro()

elif selected_page == "Correlation":
    pollution_weather_analysis()

elif selected_page == "More Correlations":
    correllation_body2()

elif selected_page == "Pollution Map":
    map_visualisation_body()

elif selected_page == "Weather Map":
    overtime_map_body()

elif selected_page == "ML Forecast":
    forecast_aqi_page()

elif selected_page == "Notebook":
    jupyter_notebook_viewer()
