import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

st.set_page_config(page_title="AQI & Weather Correlation", layout="wide")

st.title("🌍 AQI vs Weather Conditions: Correlation Overview")
st.markdown("""
This page explores how weather patterns relate to Air Quality Index (AQI) levels using:
- 📊 **Heatmaps** with correlation and statistical significance
- 🌀 **PairPlots** to show trends between AQI and weather
- 📉 **Bar Charts** showing average AQI per weather condition

Correlation is measured using the **Pearson coefficient**, ranging from -1 to 1.  
We mark correlations with:
- `*` = p < 0.05 (statistically significant)
""")
col1, col2 = st.columns(2)

@st.cache_data
def load_data():
    return pd.read_csv("Outputs//DashBoardData.zip", parse_dates=["Date"])

df = load_data()

# Column Definitions
aqi_info = [
    ("O3 Mean", "O3_AQI_Group", "Ozone (O₃)"),
    ("SO2 Mean", "SO2_AQI_Group", "Sulfur Dioxide (SO₂)"),
    ("CO Mean", "CO_AQI_Group", "Carbon Monoxide (CO)"),
    ("NO2 Mean", "NO2_AQI_Group", "Nitrogen Dioxide (NO₂)")
]

weather_cols = ["TAVG", "AWND", "PRCP", "WDMV"]
with col1:
    # 📌 Function to calculate correlation + p-value matrix
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

    # ────────────────────────────────────────────────────────────────────────────────
    # 🔥 HEATMAP SECTION
    st.header("📈 Correlation Heatmaps with Significance")

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

with col2:
    # ────────────────────────────────────────────────────────────────────────────────
    # 🌀 PAIRPLOTS SECTION
    st.header("🌀 PairPlots: AQI vs Weather")
    selected_pollutant = st.selectbox("Choose AQI Type for PairPlot", [info[2] for info in aqi_info])
    selected_cols = next((m, g) for m, g, t in aqi_info if t == selected_pollutant)

    plot_type = st.radio("Select AQI Format", ["Mean", "Group"], horizontal=True)

    pair_col = selected_cols[0] if plot_type == "Mean" else selected_cols[1]
    pair_df = df[[pair_col] + weather_cols].dropna()
    pair_df = pair_df.rename(columns={pair_col: f"{selected_pollutant} ({plot_type})"})

    st.markdown(f"Pairplot for **{selected_pollutant} ({plot_type})** and weather metrics:")

    fig = sns.pairplot(pair_df)
    st.pyplot(fig)

    # ────────────────────────────────────────────────────────────────────────────────
st.header("📉 Bar Charts: Average AQI Mean by Weather Bucket")
cola, colb, colc, cold = st.columns([1, 1, 1, 1])
with cola:
    st.write(" ")
    # 📉 BAR CHART SECTION
    selected_mean = st.selectbox("Choose AQI Mean for Bar Chart", [m for m, _, _ in aqi_info])
    bucket_metric = st.selectbox("Select Weather Metric to Bucket By", weather_cols)

    # Create quantile bins directly and assign to DataFrame
    df["WeatherBin"] = pd.qcut(df[bucket_metric], q=max(5, len(df[bucket_metric].unique())), duplicates='drop')

    # Group and compute mean AQI per bin
    bar_df = df[[selected_mean, "WeatherBin"]].dropna()
    avg_by_bin = bar_df.groupby("WeatherBin")[selected_mean].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=avg_by_bin, x="WeatherBin", y=selected_mean, ax=ax)
    ax.set_title(f"Avg {selected_mean} by {bucket_metric} Quantile Bin")
    ax.set_xlabel(bucket_metric)
    ax.set_ylabel("Average AQI Mean")
    plt.xticks(rotation=45)
    st.pyplot(fig)
with colb:
    st.write(" ")
    # 📉 BAR CHART SECTION
    selected_mean_b = st.selectbox("Choose AQI Mean for Bar Chart", [m for m, _, _ in aqi_info], index=1, key="mean_b")
    bucket_metric_b = st.selectbox("Select Weather Metric to Bucket By", weather_cols, key="mean_b2")

    # Create quantile bins directly and assign to DataFrame
    df["WeatherBin"] = pd.qcut(df[bucket_metric_b], q=max(5, len(df[bucket_metric].unique())), duplicates='drop')

    # Group and compute mean AQI per bin
    bar_df = df[[selected_mean_b, "WeatherBin"]].dropna()
    avg_by_bin = bar_df.groupby("WeatherBin")[selected_mean_b].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=avg_by_bin, x="WeatherBin", y=selected_mean_b, ax=ax)
    ax.set_title(f"Avg {selected_mean_b} by {bucket_metric_b} Quantile Bin")
    ax.set_xlabel(bucket_metric_b)
    ax.set_ylabel("Average AQI Mean")
    plt.xticks(rotation=45)
    st.pyplot(fig)
with colc:
    st.write(" ")
    selected_mean_c = st.selectbox("Choose AQI Mean for Bar Chart", [m for m, _, _ in aqi_info], index=2, key="mean_c")
    bucket_metric_c = st.selectbox("Select Weather Metric to Bucket By", weather_cols, key="mean_c2")

    # Create quantile bins directly and assign to DataFrame
    df["WeatherBin"] = pd.qcut(df[bucket_metric_c], q=max(5, len(df[bucket_metric].unique())), duplicates='drop')

    # Group and compute mean AQI per bin
    bar_df = df[[selected_mean_c, "WeatherBin"]].dropna()
    avg_by_bin = bar_df.groupby("WeatherBin")[selected_mean_c].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=avg_by_bin, x="WeatherBin", y=selected_mean_c, ax=ax)
    ax.set_title(f"Avg {selected_mean_c} by {bucket_metric_c} Quantile Bin")
    ax.set_xlabel(bucket_metric_c)
    ax.set_ylabel("Average AQI Mean")
    plt.xticks(rotation=45)
    st.pyplot(fig)
with cold:
    st.write(" ")
    selected_mean_d = st.selectbox("Choose AQI Mean for Bar Chart", [m for m, _, _ in aqi_info], index=3, key="mean_d")
    bucket_metric_d = st.selectbox("Select Weather Metric to Bucket By", weather_cols, key="metric_d")

    # Create quantile bins directly and assign to DataFrame
    df["WeatherBin"] = pd.qcut(df[bucket_metric_d], q=max(5, len(df[bucket_metric].unique())), duplicates='drop')

    # Group and compute mean AQI per bin
    bar_df = df[[selected_mean_d, "WeatherBin"]].dropna()
    avg_by_bin = bar_df.groupby("WeatherBin")[selected_mean_d].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=avg_by_bin, x="WeatherBin", y=selected_mean_d, ax=ax)
    ax.set_title(f"Avg {selected_mean_d} by {bucket_metric_d} Quantile Bin")
    ax.set_xlabel(bucket_metric_d)
    ax.set_ylabel("Average AQI Mean")
    plt.xticks(rotation=45)
    st.pyplot(fig)