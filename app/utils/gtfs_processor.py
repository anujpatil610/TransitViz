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

def process_timetable(weekly_timetable, stops, calendar):
    # Check if 'stop_name' is present in the stops DataFrame.
    if 'stop_name' not in stops.columns:
        raise KeyError("'stop_name' column is not present in the stops DataFrame.")

    # Merge to add 'Stop Name' from the stops DataFrame.
    weekly_timetable = weekly_timetable.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')

    # Check if all day columns are present in the calendar DataFrame.
    day_columns = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    if not day_columns.issubset(calendar.columns):
        raise KeyError("One or more expected day columns are not present in the calendar DataFrame.")

    # Merge with the calendar DataFrame to add day schedule information.
    weekly_timetable = weekly_timetable.merge(calendar, on='service_id', how='left')

    # Determine the schedule_days based on the days of operation.
    weekly_timetable['schedule_days'] = weekly_timetable.apply(
        lambda row: 'Mon-Fri' if all([row[day] == 1 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']]) and all([row[day] == 0 for day in ['saturday', 'sunday']])
        else 'Weekend' if all([row[day] == 1 for day in ['saturday', 'sunday']]) and all([row[day] == 0 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']])
        else 'Mixed' if any([row[day] == 1 for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']])
        else 'Other',
        axis=1
    )

    # Format the arrival and departure times to 12-hour AM/PM format.
    weekly_timetable['Arrival Time'] = pd.to_datetime(weekly_timetable['arrival_time'], errors='coerce').dt.strftime('%I:%M %p')
    weekly_timetable['Departure Time'] = pd.to_datetime(weekly_timetable['departure_time'], errors='coerce').dt.strftime('%I:%M %p')

    # Select and sort by the necessary columns for display.
    columns_to_display = ['Stop Name', 'Arrival Time', 'Departure Time', 'schedule_days']
    weekly_timetable = weekly_timetable[columns_to_display]
    weekly_timetable.sort_values(by=['Arrival Time', 'Departure Time'], inplace=True)

    return weekly_timetable

