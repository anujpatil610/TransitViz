from flask import render_template
from app import app
from app.utils.gtfs_processor import get_routes, get_stops, get_stop_times, get_trips

@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    routes = get_routes()
    stops = get_stops()
    # Other data can be loaded as needed

    # Here you might want to preprocess the data to only send necessary details to the frontend
    # For now, we'll send the full DataFrames converted to HTML tables
    routes_html = routes.to_html(classes='table table-responsive')
    stops_html = stops.to_html(classes='table table-responsive')
    
    return render_template('gtfs_dashboard.html', routes_html=routes_html, stops_html=stops_html)

# Additional routes can be created for more detailed data pages or API endpoints.



@app.route('/gps-dashboard')
def gps_dashboard():
    # Placeholder content for now
    return render_template('gps_dashboard.html', title='GPS Dashboard')
