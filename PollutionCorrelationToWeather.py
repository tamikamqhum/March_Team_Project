import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import os
from utils.theme import get_theme

theme = get_theme()

def pollution_weather_analysis():
    # st.title("🌍 ...")

    # # 🎯 Sidebar Navigation
    # with st.sidebar:
    #     selected_page = option_menu(
    #         "Navigation", 
    #         ["AQI & Weather Analysis", "Jupyter Notebook Viewer", "Pollution Map", "Weather Map", "ML Forecasting"],
    #         icons=["bar-chart", "book"],
    #         menu_icon="menu-app",
    #         default_index=0
    #     )

    # ────────────────────────────────────────────────────────────────────────────────
    # ✅ PAGE 1: AQI & Weather Analysis
    # if selected_page == "AQI & Weather Analysis":
        st.title("🌍 AQI vs Weather Conditions: Correlation Overview")
        st.markdown("""
        This page explores how weather patterns relate to Air Quality Index (AQI) levels using:
        - 📊 **Heatmaps** with correlation and statistical significance
        - 📈 **Scatter Plots** to visualize AQI vs Weather
        - 📉 **Bar Charts** showing average AQI per weather condition
        
        Correlation is measured using the **Pearson coefficient**, ranging from -1 to 1.  
        We mark correlations with:
        - `*` = p < 0.05 (statistically significant)
        """)

        # ✅ Correct CSV File Path  
        CSV_PATH = r"Outputs\DashBoardData.zip"

        @st.cache_data
        def load_data():
            """Loads AQI and Weather Data from CSV."""
            if not os.path.exists(CSV_PATH):
                st.error(f"File not found: {CSV_PATH}")
                return None
            try:
                df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
                return df
            except Exception as e:
                st.error(f"Error loading data: {e}")
                return None

        df = load_data()
        if df is None:
            st.stop()

        # 📌 COLUMN DEFINITIONS
        aqi_info = [
            ("O3 Mean", "O3_AQI_Group", "Ozone (O₃)"),
            ("SO2 Mean", "SO2_AQI_Group", "Sulfur Dioxide (SO₂)"),
            ("CO Mean", "CO_AQI_Group", "Carbon Monoxide (CO)"),
            ("NO2 Mean", "NO2_AQI_Group", "Nitrogen Dioxide (NO₂)")
        ]
        weather_cols = ["TAVG", "AWND", "PRCP", "WDMV"]

        col1, col2 = st.columns(2)

        # 🔥 HEATMAP SECTION
        with col1:
            st.header("📈 Correlation Heatmaps with Significance")

            def correlation_with_pvalues(df, target):
                results = pd.DataFrame(index=[target], columns=weather_cols)
                annotations = pd.DataFrame(index=[target], columns=weather_cols)

                for col in weather_cols:
                    series = df[[target, col]].dropna()
                    if not series.empty:
                        r, p = stats.pearsonr(series[target], series[col])
                        results.loc[target, col] = r * 100
                        annotations.loc[target, col] = f"{r * 100:.1f}{'*' if p < 0.05 else ''}"
                    else:
                        results.loc[target, col] = np.nan
                        annotations.loc[target, col] = ""

                return results.astype(float), annotations

            for label in ["Mean", "Group"]:
                st.subheader(f"🧪 AQI {label} vs Weather")
                cols = st.columns(2)

                for i, (mean_col, group_col, title) in enumerate(aqi_info):
                    aqi_col = mean_col if label == "Mean" else group_col
                    df_subset = df[[aqi_col] + weather_cols].dropna()
                    corr, annotations = correlation_with_pvalues(df_subset, aqi_col)

                    with cols[i % 2]:
                        st.markdown(f"**{title} ({label})**")
                        fig, ax = plt.subplots(figsize=(6, 1.5))
                        sns.heatmap(corr, annot=annotations, fmt="", cmap="coolwarm", center=0, ax=ax, cbar_kws={'format': '%.0f%%'})
                        ax.set_title(f"{title} ({label}) vs Weather", fontsize=10)
                        st.pyplot(fig)

        # 🔍 SCATTER PLOTS
        with col2:
            st.header("🔍 Scatter Plots: AQI vs Weather")

            selected_pollutant = st.selectbox("Choose AQI Type for Scatter Plot", [info[2] for info in aqi_info])
            selected_cols = next((m, g) for m, g, t in aqi_info if t == selected_pollutant)
            plot_type = st.radio("Select AQI Format", ["Mean", "Group"], horizontal=True)

            scatter_col = selected_cols[0] if plot_type == "Mean" else selected_cols[1]

            st.markdown(f"Scatter plots for **{selected_pollutant} ({plot_type})** and weather metrics:")
            cols = st.columns(2)

            for i, weather_var in enumerate(weather_cols):
                with cols[i % 2]:
                    fig, ax = plt.subplots()
                    sns.scatterplot(x=df[weather_var], y=df[scatter_col], alpha=0.5)
                    ax.set_title(f"{selected_pollutant} ({plot_type}) vs {weather_var}")
                    ax.set_xlabel(weather_var)
                    ax.set_ylabel(selected_pollutant)
                    st.pyplot(fig)

        # 📊 ADDITIONAL POLLUTION VISUALIZATION (Restored)
        st.header("📊 Additional Pollution Data Visualization")
        
        selected_pollutant = st.selectbox("Select a Pollutant for Bar Chart", ["Ozone (O₃)", "Sulfur Dioxide (SO₂)", "Carbon Monoxide (CO)", "Nitrogen Dioxide (NO₂)"])
        pollutant_map = {"Ozone (O₃)": "O3 Mean", "Sulfur Dioxide (SO₂)": "SO2 Mean", "Carbon Monoxide (CO)": "CO Mean", "Nitrogen Dioxide (NO₂)": "NO2 Mean"}
        selected_col = pollutant_map[selected_pollutant]

        fig, ax = plt.subplots()
        sns.histplot(df[selected_col].dropna(), kde=True, bins=30, ax=ax)
        ax.set_title(f"Distribution of {selected_pollutant}")
        ax.set_xlabel("AQI Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # ────────────────────────────────────────────────────────────────────────────────
    # ✅ PAGE 2: Jupyter Notebook Viewer
    # elif selected_page == "Jupyter Notebook Viewer":
    #     st.title("📓 Jupyter Notebook Viewer")
    #     st.markdown("This page embeds a Jupyter Notebook using **nbviewer**.")

    #     notebook_url = "https://nbviewer.org/github/Hasnain-S1/March_Team_Project-H/blob/main/jupyter_notebooks/HS-Notebook_Template.ipynb"

    #     st.markdown(f"### 📜 View the Notebook Below:")
    #     st.markdown(f"[🔗 Open in a new tab]({notebook_url})", unsafe_allow_html=True)

    #     # Embed nbviewer iframe
    #     st.components.v1.iframe(notebook_url, height=800, scrolling=True)
