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



def get_all_route_names():
    """Returns a list of all route long names."""
    routes_df = get_routes()
    return routes_df['route_long_name'].tolist()


# Additional functions can be defined to process data for specific visualizations or statistics.
