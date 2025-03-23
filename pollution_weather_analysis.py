import streamlit as st
from utils.theme import get_theme

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
