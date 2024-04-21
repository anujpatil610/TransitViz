from flask import render_template, abort
from app import app
from app.utils.gtfs_parser import load_gtfs_file

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    try:
        routes = load_gtfs_file('routes.txt')
        if routes.empty:  # Correct way to check if DataFrame is empty
            app.logger.info('No routes data available.')
            routes = None  # Optional: handle the case where no data is available
        
        # Similarly, check other DataFrames
        trips = load_gtfs_file('trips.txt')
        stops = load_gtfs_file('stops.txt')
        stop_times = load_gtfs_file('stop_times.txt')

        return render_template('gtfs_dashboard.html', routes=routes, trips=trips, stops=stops, stop_times=stop_times)
    except Exception as e:
        app.logger.error(f'Failed to load GTFS data: {e}')
        abort(500)  # Internal Server Error

@app.route('/gps-dashboard')
def gps_dashboard():
    # Placeholder content for now
    return render_template('gps_dashboard.html', title='GPS Dashboard')
