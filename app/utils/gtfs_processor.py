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

# ... (other functions)

def get_weekly_timetable_by_route_name(route_long_name):
    routes = get_routes()
    trips = get_trips()
    stop_times = get_stop_times()
    calendar = load_gtfs_file('calendar.txt')

    route_id = routes[routes['route_long_name'] == route_long_name]['route_id'].values
    if route_id.size == 0:
        return pd.DataFrame()  # No such route found

    trips_for_route = trips[trips['route_id'].isin(route_id)]
    schedule = pd.merge(stop_times, trips_for_route, on='trip_id')
    weekly_schedule = pd.merge(schedule, calendar, on='service_id')

    return weekly_schedule


# ... (other imports and functions)

def process_timetable(weekly_timetable, stops):
    calendar = load_gtfs_file('calendar.txt')
    # Merge the timetable DataFrame with the stops DataFrame to get stop names
    weekly_timetable = weekly_timetable.merge(stops, on='stop_id', how='left')
    
    # Select only the columns you want to display
    weekly_timetable = weekly_timetable[['arrival_time', 'departure_time', 'stop_name']]
    
    # Rename columns to be more user-friendly
    weekly_timetable.columns = ['Arrival Time', 'Departure Time', 'Stop Name']
    

    # Convert 'arrival_time' and 'departure_time' to datetime
    weekly_timetable['arrival_time'] = pd.to_datetime(weekly_timetable['arrival_time'], format='%H:%M:%S').dt.strftime('%I:%M %p')
    weekly_timetable['departure_time'] = pd.to_datetime(weekly_timetable['departure_time'], format='%H:%M:%S').dt.strftime('%I:%M %p')

    # Merge with the calendar DataFrame to include day information
    weekly_timetable = weekly_timetable.merge(calendar, on='service_id', how='left')

    # Create a new column for day indications, adjust according to your GTFS data structure
    weekly_timetable['schedule_days'] = weekly_timetable.apply(
        lambda row: 'Mon-Fri' if (row['monday'] == 1 and row['saturday'] == 0 and row['sunday'] == 0) 
        else 'Sat' if row['saturday'] == 1 
        else 'Sun' if row['sunday'] == 1 
        else 'Other',
        axis=1
    )

    # Select and order the columns for display
    weekly_timetable = weekly_timetable[['Stop Name', 'Arrival Time', 'Departure Time', 'schedule_days']]

    # Return the processed DataFrame
    return weekly_timetable

    # Return the processed DataFrame
    return weekly_timetable

# Remember to export this function if it's not already in the __all__ variable




def get_all_route_names():
    """Returns a list of all route long names."""
    routes_df = get_routes()
    return routes_df['route_long_name'].tolist()


# Additional functions can be defined to process data for specific visualizations or statistics.
