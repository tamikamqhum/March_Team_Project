import os
import pandas as pd
import numpy as np
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from geopy.exc import GeocoderTimedOut
import time
from geopy.geocoders import GoogleV3
from utils.simple_logger import logger, log_function_call

# Initialize the geolocator
# Load the API key from an environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise RuntimeError("Google API key not found. Please set "
                       "the GOOGLE_API_KEY environment variable.")

geolocator = GoogleV3(api_key=api_key)


# Function to extract geolocation details
def find_location_match(location, worldcities_df):
    """
    Search for a location in multiple columns of worldcities_df.

    Args:
        location (str): The location to search for.
        worldcities_df (DataFrame): The dataframe containing city data.

    Returns:
        dict: A dictionary containing the matched value, the column it was
        found in, latitude, longitude, and country.
              Returns None if no match is found.

    Example:
        location = "Denver"
        result = find_location_match(location, worldcities_df)
        print(result)
        # {'matched_value': 'Denver', 'matched_column': 'city', 'latitude': 39.7392358, 'longitude': -104.990251, 'country': 'United States'}
    """
    search_columns = ['city', 'city_ascii', 'country',
                      'iso2', 'iso3', 'admin_name']

    # Convert input to string and lowercase for case-insensitive comparison
    location = str(location).strip().lower()

    for col in search_columns:
        # Find rows where the location matches the column
        match = worldcities_df[worldcities_df[col]
                               .astype(str)
                               .str.strip()
                               .str.lower() == location]

        if not match.empty:
            # Extract the first match found
            result = {
                'matched_value': match.iloc[0][col],
                'matched_column': col,
                'latitude': match.iloc[0]['lat'],
                'longitude': match.iloc[0]['lng'],
                'country': match.iloc[0]['country']
            }
            return result

    return None  # Return None if no match is found


# Function to get geolocation information
@log_function_call(logger)
def get_geolocation_info(location):
    """
    _summary_
    # Get coordinates and formatted address from a location string
    geo_data = get_geolocation_info(address)
    print(geo_data)
    # {'latitude': 39.7785547, 'longitude': -105.0144273, 'address': '...Google full address...'}

    Args:
        location (_type_): _description_

    Returns:
        _type_: _description_
    """
    usetimedelay = True
    try:
        location_info = geolocator.geocode(location, timeout=10)
        if location_info:
            if usetimedelay:
                time.sleep(1)
            return {
                'latitude': location_info.latitude,
                'longitude': location_info.longitude,
                'address': location_info.address
            }
        else:
            if usetimedelay:
                time.sleep(1)
            return {
                'latitude': None,
                'longitude': None,
                'address': None
            }
    except GeocoderTimedOut:
        print(location)
        if usetimedelay:
            time.sleep(1)
        return {
            'latitude': None,
            'longitude': None,
            'address': None
        }
    except Exception as e:
        print(f"Geocoding error: {e}")
        if usetimedelay:
            time.sleep(1)
        return {
            'latitude': None,
            'longitude': None,
            'address': None
        }


# Function to extract geolocation details
@log_function_call(logger)
def extract_geolocation_details(address):
    """
    # Break down address into country/state/continent
    continent, country, state = extract_geolocation_details(geo_data['address'])
    print(continent, country, state)
    _summary_

    Args:
        address (_type_): _description_

    Returns:
        _type_: _description_
    """
    if address:
        address_parts = address.split(', ')
        country = address_parts[-1] if len(address_parts) > 0 else None
        state = address_parts[-2] if len(address_parts) > 1 else None
        continent = address_parts[-3] if len(address_parts) > 2 else None
        return continent, country, state
    else:
        return None, None, None


@log_function_call(logger)
def extract_locations(text, keyword_processor, nlp):
    """
    Extracts location names from text using NLP and predefined list.
    # Extract locations from text
    text = "The air quality in Sacramento and Paris is concerning."
    locations = extract_locations(text, keyword_processor, nlp)
    print(locations)
    # ['sacramento', 'paris']

    Args:
        text (_type_): _description_
        keyword_processor (_type_): _description_
        nlp (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.debug("Starting location extraction...")
    # convert text to string
    text = str(text)
    # Use NLP to extract geographic locations (GPE entities)
    doc = nlp(text)
    nlp_locations = (
        {ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"})
    logger.debug(f"NLP Extracted Locations: {nlp_locations}")

    # Fast keyword matching for known locations
    matched_locations = (
        set(keyword_processor.extract_keywords(text.lower())))
    logger.debug("Matched Locations"
                 f" from Predefined List: {matched_locations}")

    # Return matched locations if found; otherwise,
    # return NLP-extracted ones
    final_locations = (
        matched_locations if matched_locations else nlp_locations)
    logger.debug(f"Final Extracted Locations: {final_locations}")

    return list(final_locations)


@log_function_call(logger)
def restrict_api_key_server(project_id: str, key_id: str) -> Key:
    """
    Restricts the API key based on IP addresses. You can specify one or
    more IP addresses of the callers,
    for example web servers or cron jobs, that are allowed to use your API key.

    TODO(Developer): Replace the variables before running this sample.

    Args:
        project_id: Google Cloud project id.
        key_id: ID of the key to restrict. This ID is auto-created
        during key creation.
            This is different from the key string. To obtain the key_id,
            you can also use the lookup api: client.lookup_key()

    Returns:
        response: Returns the updated API Key.
    """

    # Create the API Keys client.
    client = api_keys_v2.ApiKeysClient()

    # Restrict the API key usage by specifying the IP addresses.
    # You can specify the IP addresses in IPv4 or IPv6 or a
    # subnet using CIDR notation.
    server_key_restrictions = api_keys_v2.ServerKeyRestrictions()
    server_key_restrictions.allowed_ips = ["80.189.63.110"]

    # Set the API restriction.
    # For more information on API key restriction, see:
    # https://cloud.google.com/docs/authentication/api-keys
    restrictions = api_keys_v2.Restrictions()
    restrictions.server_key_restrictions = server_key_restrictions

    key = api_keys_v2.Key()
    key.name = f"projects/{project_id}/locations/global/keys/{key_id}"
    key.restrictions = restrictions

    # Initialize request and set arguments.
    request = api_keys_v2.UpdateKeyRequest()
    request.key = key
    request.update_mask = "restrictions"

    # Make the request and wait for the operation to complete.
    response = client.update_key(request=request).result()

    print(f"Successfully updated the API key: {response.name}")
    # Use response.key_string to authenticate.
    return response

def haversine_vectorized(lat1, lon1, lat2_array, lon2_array):
    """
    Vectorized haversine distance calculation between one point and arrays of points.
    """
    R = 6371  # Earth radius in km
    lat1, lon1 = np.radians(lat1), np.radians(lon1)
    lat2, lon2 = np.radians(lat2_array), np.radians(lon2_array)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c  # Distance in km


def append_closest_location_info_bounded(
    stations_df, city_df,
    station_lat_col='lat', station_lon_col='lon',
    city_lat_col='lat', city_lon_col='lon',
    city_name_col='city',
    search_radius_km=50
):
    """
    Efficiently appends the closest city and distance to each station using bounding box + haversine.

    # Run the function
        updated_df = append_closest_location_info_bounded(
        stations_df, city_df,
        station_lat_col='lat', station_lon_col='lon',
        city_lat_col='lat', city_lon_col='lon',
        city_name_col='city',
        search_radius_km=50  # You can increase this to 100+ if needed
        )
    """

    results = []

    for _, station in stations_df.iterrows():
        lat1 = station[station_lat_col]
        lon1 = station[station_lon_col]

        # Bounding box filter
        degree_margin = search_radius_km / 111  # Rough conversion km to degrees
        lat_min, lat_max = lat1 - degree_margin, lat1 + degree_margin
        lon_min, lon_max = lon1 - degree_margin, lon1 + degree_margin

        nearby_cities = city_df[
            (city_df[city_lat_col] >= lat_min) & (city_df[city_lat_col] <= lat_max) &
            (city_df[city_lon_col] >= lon_min) & (city_df[city_lon_col] <= lon_max)
        ]

        if nearby_cities.empty:
            results.append({
                'ClosestCity': None,
                'CityDistance': None
            })
            continue

        distances = haversine_vectorized(
            lat1, lon1,
            nearby_cities[city_lat_col].values,
            nearby_cities[city_lon_col].values
        )

        min_idx = np.argmin(distances)
        closest_city = nearby_cities.iloc[min_idx][city_name_col]
        closest_distance = distances[min_idx]

        results.append({
            'ClosestCity': closest_city,
            'CityDistance': closest_distance
        })

    stations_df[['ClosestCity', 'CityDistance']] = pd.DataFrame(results)
    return stations_df