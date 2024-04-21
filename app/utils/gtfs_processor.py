import pandas as pd
import os

def load_gtfs_file(file_name):
    """Loads a specific GTFS file as a pandas DataFrame."""
    gtfs_folder = os.path.join('gtfs')  # Assuming 'gtfs' directory is at the root of your project
    file_path = os.path.join(gtfs_folder, file_name)
    return pd.read_csv(file_path)

def get_routes():
    """Returns the routes DataFrame."""
    return load_gtfs_file('routes.txt')

def get_stops():
    """Returns the stops DataFrame."""
    return load_gtfs_file('stops.txt')

def get_stop_times():
    """Returns the stop_times DataFrame."""
    return load_gtfs_file('stop_times.txt')

def get_trips():
    """Returns the trips DataFrame."""
    return load_gtfs_file('trips.txt')

# Additional functions can be defined to process data for specific visualizations or statistics.
