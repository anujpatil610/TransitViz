import os
import pandas as pd
import psycopg2
import requests
import zipfile
from psycopg2.extras import execute_values

# Environment variables for database connection
DB_NAME = os.getenv("DB_NAME", "gtfs")  # Default to 'gtfs' if not set
DB_USER = os.getenv("DB_USER", "postgres")  # Default to 'postgres' if not set
DB_PASS = os.getenv("DB_PASS")  # No default, must be set
DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to 'localhost' if not set
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to '5432' if not set

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

# Upsert data into PostgreSQL
def upsert_to_postgres(df, table_name, unique_columns):
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Prepare the INSERT INTO statement with ON CONFLICT clause
                columns = ','.join(df.columns)
                values = ','.join(['%s'] * len(df.columns))
                update_assignment = ','.join([f"{col} = EXCLUDED.{col}" for col in df.columns])
                conflict_columns = ', '.join(unique_columns)
                
                upsert_stmt = f"""
                INSERT INTO {table_name} ({columns}) VALUES ({values})
                ON CONFLICT ({conflict_columns}) DO UPDATE SET
                {update_assignment};
                """

                # Use execute_values for efficient batch inserts
                execute_values(cur, upsert_stmt, df.values)
                conn.commit()
                print(f"Data upserted into {table_name} successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Load a specific GTFS file as a pandas DataFrame
def load_gtfs_file(file_name):
    file_path = os.path.join(EXTRACTED_FOLDER, file_name)
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Strip any whitespace from headers
    return df

# Main execution
if __name__ == "__main__":
    gtfs_url = "https://passio3.com/stlawrence/passioTransit/gtfs/google_transit.zip"  # Update with actual URL
    
    # Download and extract GTFS data
    download_and_extract_gtfs_data(gtfs_url)
    
    # Define your GTFS files and corresponding database tables
    gtfs_files_to_tables = {
        'agency.txt': ('agency', ['agency_id']),
        'stops.txt': ('stops', ['stop_id']),
        'routes.txt': ('routes', ['route_id']),
        'trips.txt': ('trips', ['trip_id']),
        'stop_times.txt': ('stop_times', ['trip_id', 'stop_sequence']),
        'calendar.txt': ('calendar', ['service_id']),
        'calendar_dates.txt': ('calendar_dates', ['service_id', 'date']),
        'fare_attributes.txt': ('fare_attributes', ['fare_id']),
        'fare_rules.txt': ('fare_rules', ['fare_id', 'route_id']),  # Assuming this combination is unique
        'shapes.txt': ('shapes', ['shape_id', 'shape_pt_sequence']),
        'frequencies.txt': ('frequencies', ['trip_id', 'start_time']),
        'transfers.txt': ('transfers', ['from_stop_id', 'to_stop_id']),
        'feed_info.txt': ('feed_info', ['feed_publisher_name', 'feed_lang'])
    }
    
    # Iterate over the GTFS files and load them into the database
    for file_name, (table_name, unique_keys) in gtfs_files_to_tables.items():
        df = load_gtfs_file(file_name)
        upsert_to_postgres(df, table_name, unique_keys)
