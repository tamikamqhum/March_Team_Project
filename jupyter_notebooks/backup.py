# %%
import os
import pandas as pd
current_dir = os.getcwd()
print("initial Working directory",current_dir)
os.chdir(os.path.dirname(current_dir))
print("You set a new current directory")
current_dir = os.getcwd()
print("Final Working Dir",current_dir)

# %%
# load pollution_us_2000_2016.csv.zip
pollution = pd.read_csv('source_data/pollution_us_2000_2016.csv.zip', compression='zip')
# Drop rows with null values
pollution = pollution.dropna()
print(pollution.head())
print(pollution.info())
print(pollution.describe())
# produce summary by city, county, state, counting the number of records, and the number of unique dates add count of unique sites
pollution['Date Local'] = pd.to_datetime(pollution['Date Local'])
pollution['year'] = pollution['Date Local'].dt.year
pollution_summary = pollution.groupby(['City', 'County', 'State', 'year']).agg({'Date Local': ['count', 'nunique']})
pollution_summary.columns = ['Record Count', 'Unique Dates']
print(pollution_summary)

# %%
# produce a summary by city, county, state, min year with at lwast 350 unique dates and max year with at least 350 unique dates
pollution_summary = pollution_summary.reset_index()
pollution_summary = pollution_summary[pollution_summary['Unique Dates'] >= 350]
pollution_summary = pollution_summary.groupby(['City', 'County', 'State']).agg({'year': ['min', 'max']})
pollution_summary.columns = ['Min Year', 'Max Year']
# difference between min and max year
pollution_summary['Year Difference'] = pollution_summary['Max Year'] - pollution_summary['Min Year']
# sort on Year Difference desc
pollution_summary = pollution_summary.sort_values('Year Difference', ascending=False)

print(pollution_summary)

pollution_data_available = pollution_summary.reset_index()
pollution_data_available

# %%
# Import ghcnd-stations.txt as fixed width file using the following widths
# ID 1-11, LATITUDE 13-20, LONGITUDE 22-30, ELEVATION 32-37, STATE 39-40, NAME 42-71, GSN FLAG 73-75, HCN/CRN FLAG 77-79, WMO ID 81-85
stations_fixed = pd.read_fwf('source_data/ghcnd-stations.txt', widths=[11, 9, 10, 7, 3, 31, 4, 4, 5], header=None)
stations_fixed.columns = ['StationId', 'Latitude', 'Longitude', 'Elevation', 'StateCode', 'Name', 'GSN Flag', 'HCN/CRN Flag', 'WMO ID']
# set country to first to characters of StationId
stations_fixed['Country'] = stations_fixed['StationId'].str[:2]
stations_fixed = stations_fixed[stations_fixed['Country'] == 'US']
# load ghcnd-states.txt as fixed width file using the following widths
# STATE 1-2, NAME 4-49
states_fixed = pd.read_fwf('source_data/ghcnd-states.txt', widths=[2, 46], header=None)
states_fixed.columns = ['StateCode', 'State']
print("states_fixed", states_fixed.head())
print("stations_fixed", stations_fixed.head())
# match the state name to the state abbreviation
stations_fixed = pd.merge(stations_fixed, states_fixed, on='StateCode')
print("stations_fixed_post_merge",stations_fixed.head())

# %%
# print pollution_summary columns
print(pollution_summary.columns)
print(pollution_summary.head())
# print states_fixed columns
print(states_fixed.columns)
print(states_fixed.head())
# print stations_fixed columns
print(stations_fixed.columns)
print(stations_fixed.head())

# %%
# match the state column in pollution_summary to State frp, states_fixed, convert state to upper case for better matching
# Ensure 'State' columns in both dataframes are in uppercase and stripped of leading/trailing spaces for consistent matching
pollution_summary = pollution_summary.reset_index()  # Reset index to access 'State' column directly
pollution_summary['State'] = pollution_summary['State'].str.upper().str.strip()
states_fixed['State'] = states_fixed['State'].str.upper().str.strip()
# merge pollution_summary with states_fixed
pollution_summary_inc_sc = pd.merge(pollution_summary, states_fixed, left_on='State', right_on='State')
print("pollution_summary_post_merge", pollution_summary_inc_sc.head())
# add column to states_fixed with the number of stations in each state
stations_fixed_gb = stations_fixed.groupby(['StateCode', 'State'])['StationId'].count().reset_index()
stations_fixed_gb.columns = ['StateCode', 'State', 'Station Count']
print("stations_fixed_station_count", stations_fixed_gb.head())
# add the station count to the pollution_summary
pollution_summary_stat_count = pd.merge(pollution_summary_inc_sc, stations_fixed_gb, on='StateCode')
print("pollution_summary_ merge2", pollution_summary_stat_count.head())
# add the station count to the states_fixed
states_fixed = pd.merge(states_fixed, stations_fixed_gb, on='State')
print("states_fixed_stations_merge", states_fixed.head())
# sort states_fixed by Station Count desc
states_fixed = states_fixed.sort_values('Station Count', ascending=False)
print("states_fixed_sort", states_fixed)

pollution_summary_stat_count

# %%
# generate a list of stationId for those states with 10 or more years of data
states_10_years = pollution_summary_stat_count[pollution_summary_stat_count['Year Difference'] >= 10]


# %%
station_list = states_10_years['StationId'].tolist()
station_list


