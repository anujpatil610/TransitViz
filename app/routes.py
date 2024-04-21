from flask import render_template, request
from app import app
from app.utils.gtfs_processor import (
    get_routes, get_stops, get_stop_times, get_trips, get_calendar,
    get_weekly_timetable_by_route_name, get_all_route_names,
    process_timetable  # make sure this is properly imported
)

@app.route('/')
def index():
    # Pass the list of route names to the homepage for the dropdown
    route_names = get_all_route_names()
    return render_template('index.html', title='Home', route_names=route_names)

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    routes = get_routes()
    stops = get_stops()
    routes_html = routes.to_html(classes='table table-responsive')
    stops_html = stops.to_html(classes='table table-responsive')
    return render_template('gtfs_dashboard.html', routes_html=routes_html, stops_html=stops_html)

@app.route('/timetable', methods=['GET'])
def timetable():
    route_names = get_all_route_names()
    selected_route_name = request.args.get('route_name', None)
    timetable_html = ""

    if selected_route_name:
        weekly_timetable = get_weekly_timetable_by_route_name(selected_route_name)
        if not weekly_timetable.empty:
            stops = get_stops()  # Load stops data
            calendar = get_calendar()  # Load calendar data
            # Ensure all required data is correctly merged or included before processing
            weekly_timetable = weekly_timetable.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')
            try:
                processed_timetable = process_timetable(weekly_timetable, stops, calendar)  # Pass calendar as well
                timetable_html = processed_timetable.to_html(index=False, classes='table table-responsive')
            except KeyError as e:
                timetable_html = f"<div class='alert alert-danger'>Error in processing timetable data: {e}</div>"
        else:
            timetable_html = "<div class='alert alert-warning'>No timetable available for this route.</div>"
    else:
        timetable_html = "<div class='alert alert-info'>Please select a route to view the timetable.</div>"

    return render_template('timetable.html', timetable_html=timetable_html, route_names=route_names)

@app.route('/gps-dashboard')
def gps_dashboard():
    return render_template('gps_dashboard.html', title='GPS Dashboard')
