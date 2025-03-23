
from weather_processor import process_weather_files

files_to_process = ["2000.csv.gz",
                    "2001.csv.gz",
                    "2002.csv.gz",
                    "2003.csv.gz",
                    "2004.csv.gz",
                    "2005.csv.gz",
                    "2006.csv.gz",
                    "2007.csv.gz",
                    "2008.csv.gz",
                    "2009.csv.gz",
                    "2010.csv.gz",
                    "2011.csv.gz",
                    "2012.csv.gz",
                    "2013.csv.gz",
                    "2014.csv.gz",
                    "2015.csv.gz",
                    "2016.csv.gz",
                    ]
process_weather_files(
    file_list=files_to_process,
    config_path="config/element_config.json",
    stations_file="Outputs/Us_Stations_with_City_100km.csv",
    output_dir="Not_to_be_shared_to_repo"
)
