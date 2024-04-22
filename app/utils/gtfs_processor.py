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

def process_timetable(weekly_timetable, stops, calendar):
    # Ensure all data types for stop_id are consistent
    weekly_timetable['stop_id'] = weekly_timetable['stop_id'].astype(str).str.strip()
    stops['stop_id'] = stops['stop_id'].astype(str).str.strip()

    # Align columns before merging to avoid 'Operands are not aligned' error
    weekly_timetable, stops = weekly_timetable.align(stops, axis=1, copy=False)

    # Perform the merge to add 'Stop Name' from the stops DataFrame
    merged_timetable = weekly_timetable.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')

    # Immediately check the result of the merge
    if merged_timetable['stop_name'].isna().any():
        print("Issues detected post-merge: Missing 'stop_name' entries found.")
        problematic_ids = merged_timetable[merged_timetable['stop_name'].isna()]['stop_id'].unique()
        print(f"Problematic 'stop_id's: {problematic_ids}")
        # Also print the stops that were supposed to match but didn't
        print("Entries in 'stops' DataFrame that should have matched:")
        print(stops[stops['stop_id'].isin(problematic_ids)])

    # Merge calendar data
    merged_timetable = merged_timetable.merge(calendar, on='service_id', how='left')
    if 'monday' not in merged_timetable.columns:
        raise KeyError("'monday' column is missing after merging with calendar DataFrame.")

    # Process schedule days based on the calendar
    merged_timetable['schedule_days'] = merged_timetable.apply(
        lambda row: 'Mon-Fri' if all(row[day] == 1 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
        else 'Weekend' if row['saturday'] == 1 and row['sunday'] == 1
        else 'Mixed',
        axis=1
    )

    # Format the times for display
    merged_timetable['Arrival Time'] = pd.to_datetime(merged_timetable['arrival_time'], errors='coerce').dt.strftime('%I:%M %p')
    merged_timetable['Departure Time'] = pd.to_datetime(merged_timetable['departure_time'], errors='coerce').dt.strftime('%I:%M %p')

    # Sort the timetable by days and times
    merged_timetable.sort_values(by=['schedule_days', 'Arrival Time', 'Departure Time'], inplace=True)

    # Select the columns to display
    columns_to_display = ['stop_name', 'Arrival Time', 'Departure Time', 'schedule_days']
    final_timetable = merged_timetable[columns_to_display]
    
    return final_timetable


















