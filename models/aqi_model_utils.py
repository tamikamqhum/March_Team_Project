
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Define model paths
MODEL_DIR = Path("ML_Models")
COMPRESSED_MODELS = {
    "O3_AQI_Group": MODEL_DIR / "rf_model_O3_AQI_Group_grouped_compressed.pkl",
    "SO2_AQI_Group": MODEL_DIR / "rf_model_SO2_AQI_Group_grouped_compressed.pkl",
    "CO_AQI_Group": MODEL_DIR / "rf_model_CO_AQI_Group_grouped_compressed.pkl",
    "NO2_AQI_Group": MODEL_DIR / "rf_model_NO2_AQI_Group_grouped_compressed.pkl"
}

# Load all models into memory
MODELS = {target: joblib.load(path) for target, path in COMPRESSED_MODELS.items()}

# Define the features used for prediction
FEATURES = [
    "Year", "Month", "Day", "DayOfWeek", "DayOfYear", "DayOfYear_cos", "DayOfYear_sin",
    "TAVG", "TMAX", "TMIN", "PRCP", "AWND", "WDMV",
    "CityDistance", "WS_Elevation", "WS_Latitude", "WS_Longitude",
    "WT_Precip", "WT_Wind", "WT_Extreme", "WT_Other"
]

def prepare_input(date, weather_data):
    date = pd.to_datetime(date)
    features = {
        "Year": date.year,
        "Month": date.month,
        "Day": date.day,
        "DayOfWeek": date.dayofweek,
        "DayOfYear": date.dayofyear,
        "DayOfYear_cos": np.cos(2 * np.pi * date.dayofyear / 365),
        "DayOfYear_sin": np.sin(2 * np.pi * date.dayofyear / 365),
        **weather_data
    }

    # Create DataFrame and enforce correct column order
    df = pd.DataFrame([features])
    df = df[FEATURES]  # ✅ THIS LINE ENSURES CORRECT ORDER
    return df

def predict_aqi_group(target, input_df):
    model = MODELS.get(target)
    if model:
        return model.predict(input_df)[0]
    return None


def get_model_metadata(target):
    model = MODELS.get(target)
    if not model:
        return {}

    clf = model.named_steps["clf"]
    metadata = {
        "classes": list(clf.classes_),
        "feature_importances": dict(zip(FEATURES, clf.feature_importances_))
    }
    return metadata
