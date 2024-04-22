import pandas as pd
import os

def load_gtfs_file(file_name):
    """Loads a specific GTFS file as a pandas DataFrame."""
    gtfs_folder = os.path.join('gtfs')  # Assuming 'gtfs' directory is at the root of your project
    file_path = os.path.join(gtfs_folder, file_name)
    df = pd.read_csv(file_path, dtype={
        'service_id': str,
        'monday': int, 'tuesday': int, 'wednesday': int,
        'thursday': int, 'friday': int, 'saturday': int, 'sunday': int,
        'start_date': str, 'end_date': str
    })
    print(f"Loaded {file_name} with columns: {df.columns.tolist()}")  # Debugging statement
    return df


def get_calendar():
    """Preprocesses and returns the calendar DataFrame."""
    calendar_df = load_gtfs_file('calendar.txt')
    # Preprocess calendar_df if needed, for example:
    calendar_df['service_id'] = calendar_df['service_id'].astype(str).str.strip()
    return calendar_df

def get_routes():
    return load_gtfs_file('routes.txt')

def get_stops():
    return load_gtfs_file('stops.txt')

def get_stop_times():
    return load_gtfs_file('stop_times.txt')

def get_trips():
    return load_gtfs_file('trips.txt')

def get_all_route_names():
    """Returns a list of all route long names."""
    routes_df = get_routes()
    return routes_df['route_long_name'].drop_duplicates().sort_values().tolist()

def get_weekly_timetable_by_route_name(route_long_name):
    """Generates a weekly timetable DataFrame for a given route."""
    routes = get_routes()
    route_id = routes.loc[routes['route_long_name'].str.lower() == route_long_name.lower(), 'route_id']
    if route_id.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no route is found

    trips = get_trips()
    trips_for_route = trips[trips['route_id'].isin(route_id)]
    stop_times = get_stop_times()
    schedule = pd.merge(stop_times, trips_for_route, on='trip_id')
    calendar = get_calendar()
    weekly_schedule = pd.merge(schedule, calendar, on='service_id', how='left')
    return weekly_schedule

import pandas as pd

import pandas as pd

import pandas as pd

import pandas as pd

def process_timetable(weekly_timetable, stops, calendar):
    # Ensure data types are consistent and appropriate for merging
    weekly_timetable['stop_id'] = weekly_timetable['stop_id'].astype(str).str.strip()
    stops['stop_id'] = stops['stop_id'].astype(str).str.strip()

    # Validate presence of 'stop_name' in 'stops' DataFrame
    if 'stop_name' not in stops.columns:
        raise Exception("'stop_name' column missing from stops DataFrame.")
    if stops['stop_name'].isna().any():
        raise Exception("Null 'stop_name' values found in stops DataFrame.")

    # Fill any nulls in 'stop_name' to prevent issues post-merge
    stops['stop_name'].fillna('Missing Stop Name', inplace=True)

    # Merge to add 'Stop Name' from the stops DataFrame.
    merged_timetable = weekly_timetable.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')
    if merged_timetable['stop_name'].isna().any():
        raise Exception("Merge failed to map some 'stop_id' to 'stop_name'. Please check data consistency.")

    # Merge calendar data
    merged_timetable = merged_timetable.merge(calendar, on='service_id', how='left')
    if 'monday' not in merged_timetable.columns:
        raise KeyError("'monday' column is missing after merging with calendar DataFrame.")

    # Calculate 'schedule_days' based on operational days
    merged_timetable['schedule_days'] = merged_timetable.apply(
        lambda row: 'Mon-Fri' if all(row[day] == 1 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']) 
        else 'Weekend' if row['saturday'] == 1 and row['sunday'] == 1 
        else 'Mixed',
        axis=1
    )

    # Convert times and format them
    merged_timetable['Arrival Time'] = pd.to_datetime(merged_timetable['arrival_time'], errors='coerce').dt.strftime('%I:%M %p')
    merged_timetable['Departure Time'] = pd.to_datetime(merged_timetable['departure_time'], errors='coerce').dt.strftime('%I:%M %p')

    # Sort by 'schedule_days' and time
    merged_timetable.sort_values(by=['schedule_days', 'Arrival Time', 'Departure Time'], inplace=True)

    # Prepare final display table
    columns_to_display = ['stop_name', 'Arrival Time', 'Departure Time', 'schedule_days']
    final_timetable = merged_timetable[columns_to_display]

    return final_timetable

# Now, this function includes rigorous checks for data integrity and explicitly handles potential null values in 'stop_name'.










