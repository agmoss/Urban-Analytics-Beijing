import glob
import os
import folium
import pandas as pd

from scripts import map_visualization as mv
from scripts import process_data as process


def path_config():
    """Setup read and write filepaths"""

    import json

    with open('config.json', 'r') as f:
        config = json.load(f)

    read_path = config['FILE_PATHS']['read_data']
    write_path = config['FILE_PATHS']['write_output']

    return read_path, write_path


def main(config):
    """Main method for creating the heatmap"""

    read_path, write_path = config()

    # File path extension
    ext = "*.txt"

    # Create a list of file paths for the map function
    file_list = glob.glob(os.path.join(read_path, ext))

    # Convert file paths to a list of dataframes
    df_list = process.Mapper.mult_map(process.Mapper.list_to_df, file_list)

    # Concatenate the dataframe lists into one dataframe 
    df = pd.concat(df_list)

    # Take sample for visual
    df = df.sample(frac=0.6, replace=True)

    # Clean index
    df.reset_index(inplace=True, drop=True)

    # Create a folium map object
    mp = folium.Map([39.9042, 116.4074], zoom_start=10)

    # Pass the folium map to the user defined LocationMap class
    heat_map = mv.LocationMap("Folium heat map", mp)

    # Add the data to the map
    heat_map.add_heat(df)

    # Save the map
    heat_map.fmap.save(write_path + "beijing.html")


if __name__ == '__main__':
    print(__name__)
    main(path_config)
