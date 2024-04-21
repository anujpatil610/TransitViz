from flask import render_template
from app import app
from app.utils.gtfs_processor import get_routes, get_stops, get_stop_times, get_trips
from app.utils.gtfs_processor import get_weekly_timetable_by_route_name
from flask import render_template, request
from app.utils.gtfs_processor import get_all_route_names


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

@app.route('/timetable', methods=['GET'])
def timetable():
    route_names = get_all_route_names()
    route_name = request.args.get('route_name', None)
    timetable_html = ""

    if route_name:
        weekly_timetable = get_weekly_timetable_by_route_name(route_name)
        if not weekly_timetable.empty:
            timetable_html = weekly_timetable.to_html(classes='table table-responsive')
        else:
            timetable_html = "<div class='alert alert-warning'>No timetable available for this route.</div>"

    return render_template('timetable.html', route_names=route_names, timetable_html=timetable_html)

@app.route('/gps-dashboard')
def gps_dashboard():
    # Placeholder content for now
    return render_template('gps_dashboard.html', title='GPS Dashboard')
