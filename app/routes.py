from app import app
from flask import render_template
from app.utils.gtfs_parser import load_gtfs_file

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    # Load necessary GTFS data files
    routes = load_gtfs_file('routes.txt')
    trips = load_gtfs_file('trips.txt')
    stops = load_gtfs_file('stops.txt')
    stop_times = load_gtfs_file('stop_times.txt')

    # Example: Process and pass data to the template
    # This is where you can perform more complex data manipulations and joins

    return render_template('gtfs_dashboard.html', routes=routes, trips=trips, stops=stops, stop_times=stop_times)
