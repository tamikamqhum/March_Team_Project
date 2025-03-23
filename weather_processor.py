
import os
import json
import logging
import pandas as pd
from typing import List
from tqdm import tqdm

# Set up logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("weather_processing.log"),
        logging.StreamHandler()
    ]
)

def load_element_config(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return json.load(f)

def process_weather_files(
    file_list: List[str],
    config_path: str,
    stations_file: str,
    output_dir: str
) -> None:
    element_agg_map = load_element_config(config_path)
    element_list = list(element_agg_map.keys())
    station_df = pd.read_csv(stations_file)
    station_ids = set(station_df["StationId"])

    for file in tqdm(file_list, desc="Processing files"):
        filepath = os.path.join("Not_to_be_shared_to_repo", file)
        logging.info(f"Reading file: {filepath}")

        weather_df = pd.read_csv(
            filepath,
            header=None,
            usecols=[0, 1, 2, 3],
            names=["Station_ID", "Date", "Element", "DataValue"]
        )

        logging.info(f"Initial shape: {weather_df.shape}")
        weather_df = weather_df[
            (weather_df["Station_ID"].str[:2] == "US") &
            (weather_df["Station_ID"].isin(station_ids)) &
            (weather_df["Element"].isin(element_list)) &
            (weather_df["DataValue"] != 9999)
        ]
        logging.info(f"Filtered shape: {weather_df.shape}")

        weather_df["AggType"] = weather_df["Element"].map(element_agg_map)
        pivoted_dfs = []

        for agg_func in ["mean", "max", "min"]:
            sub_df = weather_df[weather_df["AggType"] == agg_func]
            if not sub_df.empty:
                pivot = sub_df.pivot_table(
                    index=["Station_ID", "Date"],
                    columns="Element",
                    values="DataValue",
                    aggfunc=agg_func
                )
                pivoted_dfs.append(pivot)

        final_df = pd.concat(pivoted_dfs, axis=1).reset_index()
        logging.info(f"Final shape: {final_df.shape}")

        output_file = f"Us_{file}_Weather_Unpacked.zip"
        output_path = os.path.join(output_dir, output_file)
        final_df.to_csv(output_path, index=False, compression="zip")
        logging.info(f"Saved output to: {output_path}")
