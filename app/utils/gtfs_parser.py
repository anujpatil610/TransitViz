import os
import pandas as pd
import psycopg2
import requests
import zipfile
from psycopg2.extras import execute_values

# Environment variables for database connection
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Path to the directory where you want to extract GTFS files
EXTRACTED_FOLDER = 'gtfs'

# Establish a database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASS, 
        host=DB_HOST, 
        port=DB_PORT
    )

# Download and extract GTFS data
def download_and_extract_gtfs_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        zip_file_path = os.path.join(EXTRACTED_FOLDER, 'gtfs_data.zip')
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(EXTRACTED_FOLDER)
        print("GTFS data downloaded and extracted.")
    else:
        print(f"Failed to download GTFS data, status code: {response.status_code}")

# Load and update data into PostgreSQL
def load_to_postgres(df, table_name):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            # Clear existing data
            cur.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")

            # Prepare the INSERT INTO statement
            columns = ','.join(df.columns)
            values = ','.join(['%s'] * len(df.columns))
            insert_stmt = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            # Use execute_values for efficient batch inserts
            execute_values(cur, insert_stmt, df.values)
            conn.commit()
            print(f"Data loaded into {table_name} successfully.")

# Load a specific GTFS file as a pandas DataFrame
def load_gtfs_file(file_name):
    file_path = os.path.join(EXTRACTED_FOLDER, file_name)
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Strip any whitespace from headers
    return df

# Main execution
if __name__ == "__main__":
    gtfs_url = "https://passio3.com/stlawrence/passioTransit/gtfs/google_transit.zip"
    
    # Download and extract GTFS data
    download_and_extract_gtfs_data(gtfs_url)
    
    # Define your GTFS files and corresponding database tables
    gtfs_files_to_tables = {
        'stops.txt': 'stops',
        'routes.txt': 'routes',
        # Add other GTFS files and tables as necessary
    }
    
    # Iterate over the GTFS files and load them into the database
    for file_name, table_name in gtfs_files_to_tables.items():
        df = load_gtfs_file(file_name)
        load_to_postgres(df, table_name)
