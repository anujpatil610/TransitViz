import requests
import zipfile
import os
import pandas as pd

def download_gtfs_data(url):
    """Downloads and extracts GTFS data from a given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        # Save the zip file
        with open('gtfs.zip', 'wb') as f:
            f.write(response.content)

        # Extract the zip file
        with zipfile.ZipFile('gtfs.zip', 'r') as zip_ref:
            zip_ref.extractall('gtfs')

        print("GTFS data downloaded and extracted.")
    else:
        print("Failed to download GTFS data.")

def load_gtfs_file(file_name):
    """Loads a specific GTFS file as a pandas DataFrame."""
    file_path = os.path.join('gtfs', file_name)
    return pd.read_csv(file_path)

if __name__ == "__main__":
    gtfs_url = "https://passio3.com/stlawrence/passioTransit/gtfs/google_transit.zip"
    download_gtfs_data(gtfs_url)
