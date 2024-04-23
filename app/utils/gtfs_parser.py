import os
import pandas as pd
import psycopg2
import requests
import zipfile
from psycopg2.extras import execute_values

# Environment variables for database connection
DB_NAME = os.getenv("DB_NAME", "gtfs")  # Default to 'gtfs' if not set
DB_USER = os.getenv("DB_USER", "postgres")  # Default to 'postgres' if not set
DB_PASS = os.getenv("DB_PASS", "H3ADSHOT")  # Ensure this is set as an environment variable
DB_HOST = os.getenv("DB_HOST", "localhost")  # Default to 'localhost' if not set
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to '5432' if not set

# Path to the directory where you want to extract GTFS files
EXTRACTED_FOLDER = 'gtfs'

# Ensure the EXTRACTED_FOLDER exists
if not os.path.exists(EXTRACTED_FOLDER):
    os.makedirs(EXTRACTED_FOLDER)

# Establish a database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASS, 
        host=DB_HOST, 
        port=DB_PORT
    )

# Load a specific GTFS file as a pandas DataFrame
def load_gtfs_file(file_name):
    file_path = os.path.join(EXTRACTED_FOLDER, file_name)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        # Handle the missing file as appropriate, e.g., skip processing or alert the user

def upsert_to_postgres(df, table_name, unique_columns):
    if df is None:
        print(f"Skipping upsert for {table_name} as DataFrame is None")
        return

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Prepare the INSERT INTO statement with ON CONFLICT clause
                columns = ','.join(['"' + col + '"' for col in df.columns])
                values_placeholders = ','.join(['%s'] * len(df.columns))
                update_assignment = ','.join([f'"{col}" = EXCLUDED."{col}"' for col in unique_columns])
                conflict_columns = ','.join(['"' + col + '"' for col in unique_columns])
                
                # Construct the SQL statement
                sql = f"""
                INSERT INTO "{table_name}" ({columns})
                VALUES ({values_placeholders})
                ON CONFLICT ({conflict_columns})
                DO UPDATE SET
                {update_assignment}
                """
                
                # Convert DataFrame rows to a list of tuples
                data_tuples = [tuple(x) for x in df.to_numpy()]
                
                # Debugging output
                print("SQL Command:", sql)
                #print("Data Tuples:", data_tuples)

                # Use execute_values to perform the upsert operation
                execute_values(cur, sql, data_tuples)
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        # Additional debugging output
        print("SQL Command that caused the error:", sql)
        #print("Data Tuples that caused the error:", data_tuples)
    finally:
        conn.close()






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

if __name__ == "__main__":
    gtfs_url = "https://passio3.com/stlawrence/passioTransit/gtfs/google_transit.zip"  # Update with actual URL
    download_and_extract_gtfs_data(gtfs_url)

    # Example usage
    file_names = ['agency.txt', 'stops.txt', 'routes.txt', 'trips.txt', 'stop_times.txt', 
                  'fare_attributes.txt', 'fare_rules.txt', 'shapes.txt', 'frequencies.txt', 
                  'transfers.txt', 'feed_info.txt']

    for file_name in file_names:
        df = load_gtfs_file(file_name)
        if df is not None:
            upsert_to_postgres(df, file_name[:-4], ['id'])  # Assuming 'id' is a unique column
