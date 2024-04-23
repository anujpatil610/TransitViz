import os
import csv
import psycopg2
import pandas as pd
from contextlib import contextmanager
from psycopg2.extras import execute_values

EXTRACTED_FOLDER = 'gtfs'  # Update with the relative path to your extracted folder

@contextmanager
def get_cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
    except Exception as e:
        connection.rollback()
        raise e
    else:
        connection.commit()
    finally:
        cursor.close()

def connect_db():
    # Update the connection parameters as needed
    conn = psycopg2.connect(
        host='localhost',
        database='gtfs',
        user='postgres',
        password='H3ADSHOT'
    )
    return conn

def load_gtfs_file(file_name):
    file_path = os.path.join(EXTRACTED_FOLDER, file_name)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def import_gtfs_data(table_name, file_path, columns, conflict_columns):
    conn = connect_db()
    if conn is not None:
        try:
            with get_cursor(conn) as cur:
                # Drop the existing table if it exists
                cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                conn.commit()

                # Create a new table with proper SQL data types
                cur.execute(f"""
                    CREATE TABLE {table_name} (
                        {columns}
                    );
                """)
                conn.commit()

                # Add a unique constraint to the table
                if table_name == 'shapes':
                    cur.execute(f"""
                        ALTER TABLE {table_name}
                        ADD CONSTRAINT shapes_unique UNIQUE (shape_id, shape_pt_sequence);
                    """)
                    conn.commit()

                # Check if the file exists before attempting to import
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        # Prepare the data for insertion
                        data = [tuple(row.values()) for row in reader]
                        # Prepare the INSERT statement
                        insert_query = f"""
                            INSERT INTO {table_name} ({','.join(reader.fieldnames)})
                            VALUES ({','.join(['%s'] * len(reader.fieldnames))})
                            ON CONFLICT ({conflict_columns}) DO NOTHING;
                        """
                        # Execute the INSERT statement
                        psycopg2.extras.execute_batch(cur, insert_query, data)
                    print(f"Data imported successfully into {table_name}")
                else:
                    print(f"File {file_path} does not exist. Skipping import for {table_name}.")
        except Exception as e:
            print(f"An error occurred during data import: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")







if __name__ == "__main__":
    gtfs_files = [
        ('agency', 'agency.txt', 
         'agency_id SERIAL PRIMARY KEY, agency_name VARCHAR(255), agency_url VARCHAR(255), '
         'agency_timezone VARCHAR(255), agency_lang VARCHAR(2), agency_phone VARCHAR(50), '
         'agency_fare_url VARCHAR(255), agency_email VARCHAR(255)', 
         'agency_id'),

        ('calendar', 'calendar.txt', 
         'service_id REAL PRIMARY KEY, monday INTEGER, tuesday INTEGER, wednesday INTEGER, '
         'thursday INTEGER, friday INTEGER, saturday INTEGER, sunday INTEGER, '
         'start_date DATE, end_date DATE', 
         'service_id'),

        ('calendar_dates', 'calendar_dates.txt', 
         'service_id REAL, date DATE, exception_type INTEGER, '
         'PRIMARY KEY (service_id, date)', 
         'service_id, date'),

        ('feed_info', 'feed_info.txt', 
         'feed_publisher_name VARCHAR(255) PRIMARY KEY, feed_publisher_url VARCHAR(255), feed_lang VARCHAR(2)', 
         'feed_publisher_name'),

        ('routes', 'routes.txt', 
         'route_id SERIAL PRIMARY KEY, agency_id INTEGER, route_short_name VARCHAR(50), '
         'route_long_name VARCHAR(255), route_type INTEGER, route_color VARCHAR(6), '
         'route_text_color VARCHAR(6)', 
         'route_id'),

        ('shapes', 'shapes.txt', 
         'shape_id INTEGER, shape_pt_lat NUMERIC(10, 6), shape_pt_lon NUMERIC(10, 6), '
         'shape_pt_sequence INTEGER, PRIMARY KEY(shape_id, shape_pt_sequence)', 
         'shape_id, shape_pt_sequence'),
        
        ('stop_times', 'stop_times.txt', 
        'trip_id INTEGER, arrival_time TIME, departure_time TIME, stop_id INTEGER, '
        'stop_sequence INTEGER, stop_headsign VARCHAR(255), pickup_type NUMERIC, '
        'drop_off_type NUMERIC, timepoint NUMERIC, '
        'PRIMARY KEY (trip_id, stop_sequence)', 
        'trip_id, stop_sequence'),
    
        ('stops', 'stops.txt', 
        'stop_id SERIAL PRIMARY KEY, stop_code VARCHAR(50), stop_name VARCHAR(255), '
        'stop_desc TEXT, stop_lat NUMERIC(10, 6), stop_lon NUMERIC(10, 6), '
        'stop_url VARCHAR(255), location_type INTEGER, stop_timezone VARCHAR(50), '
        'wheelchair_boarding INTEGER, platform_code VARCHAR(50)', 
        'stop_id'),
    
        ('trips', 'trips.txt', 
        'route_id INTEGER, service_id NUMERIC, trip_id SERIAL PRIMARY KEY, '
        'trip_headsign VARCHAR(255), trip_short_name VARCHAR(50), direction_id NUMERIC, '
        'block_id NUMERIC, shape_id INTEGER, wheelchair_accessible INTEGER, bikes_allowed INTEGER', 
        'trip_id')
]
    

    for table_name, file_name, columns, conflict_columns in gtfs_files:
        df = load_gtfs_file(file_name)
        import_gtfs_data(df, table_name, columns, conflict_columns)
