import zipfile
import os
import pandas as pip
import requests
import pandas as pd

# Path to the directory where you want to extract GTFS files
EXTRACTED_FOLDER = 'gtfs'

def download_and_extract_gtfs_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Assuming the response content is the zip file
        zip_file_path = os.path.join(EXTRACTED_FOLDER, 'gtfs_data.zip')
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        # Extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(EXTRACTED_FOLDER)
        print("GTFS data downloaded and extracted.")
    else:
        print("Failed to download GTFS data.")

def load_gtfs_file(file_name):
    """Loads a specific GTFS file as a pandas DataFrame."""
    file_path = os.path.join(EXTRACTED_FOLDER, file_name)
    return pd.read_csv(file_path)

# Example usage
if __name__ == "__main__":
    gtfs_url = "https://passio3.com/stlawrence/passioTransit/gtfs/google_transit.zip"
    download_and_extract_gtfs_data(gtfs_url)