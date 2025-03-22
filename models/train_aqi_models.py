import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
import joblib

# === Load your main dataset ===
df = pd.read_csv("Outputs/DashBoardData.zip", low_memory=False)

# === Parse and engineer date features ===
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["DayOfYear"] = df["Date"].dt.dayofyear
df["DayOfYear_cos"] = np.cos(2 * np.pi * df["DayOfYear"] / 365)
df["DayOfYear_sin"] = np.sin(2 * np.pi * df["DayOfYear"] / 365)

# === Group WT weather features ===
df["WT_Precip"] = df[["WT08", "WT02", "WT09", "WT11"]].sum(axis=1)
df["WT_Wind"] = df[["WT06", "WT13"]].sum(axis=1)
df["WT_Extreme"] = df[["WT18", "WT22"]].sum(axis=1)
df["WT_Other"] = df[["WT01", "WT02", "WT04", "WT05", "WT03", "WT16"]].sum(axis=1)

# === Define features and targets ===
features = [
    "Year", "Month", "Day", "DayOfWeek", "DayOfYear",
    "DayOfYear_cos", "DayOfYear_sin", "TAVG", "TMAX", "TMIN",
    "PRCP", "AWND", "WDMV", "CityDistance", "WS_Elevation",
    "WS_Latitude", "WS_Longitude", "WT_Precip", "WT_Wind", "WT_Extreme", "WT_Other"
]
targets = ["O3_AQI_Group", "SO2_AQI_Group", "CO_AQI_Group", "NO2_AQI_Group"]

# === Create output folder for models ===
output_dir = "models"
os.makedirs(output_dir, exist_ok=True)

# === Train and compress each model ===
for target in targets:
    df_clean = df.dropna(subset=features + [target])
    X = df_clean[features]
    y = df_clean[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", PowerTransformer()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    model_path = os.path.join(output_dir, f"rf_model_{target}_grouped_compressed.pkl")
    joblib.dump(pipeline, model_path, compress=3)

    print(f"✅ Saved: {model_path}")
