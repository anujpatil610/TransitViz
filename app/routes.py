from flask import render_template
from app import app, db

from flask import jsonify

from app.models import Route, Stop, Trip

@app.route('/')
def index():
    # Fetch all route names for the dropdown menu from the database
    
    return render_template('index.html')

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    routes = Route.query.all()
    num_routes = Route.query.count()
    num_stops = Stop.query.count()
    return render_template('gtfs_dashboard.html', routes=routes, num_routes=num_routes, num_stops=num_stops)


@app.route('/gps-dashboard')
def gps_dashboard():
    # This page is not implemented yet and the link is disabled in the template
    return render_template('gps_dashboard.html', title='GPS Dashboard (Coming Soon)')


@app.route('/timetable', methods=['GET'])
def timetable():
    # Obtain the list of all route long names to pass back to the dropdown in case of form re-render
    

    return render_template('timetable.html')

@app.route('/api/routes')
def api_routes():
    data = Route.query.with_entities(Route.route_id, Route.route_long_name).all()
    return jsonify([{'route_id': route[0], 'route_long_name': route[1]} for route in data])

@app.route('/api/stops')
def api_stops():
    data = Stop.query.with_entities(Stop.stop_id, Stop.stop_name, Stop.stop_lat, Stop.stop_lon).all()
    return jsonify([{'stop_id': stop[0], 'stop_name': stop[1], 'lat': stop[2], 'lon': stop[3]} for stop in data])

@app.route('/api/routes/stats')
def route_stats():
    from sqlalchemy import func
    stats = db.session.query(
        Route.route_short_name, 
        func.count(Trip.id).label('trip_count')
    ).join(Trip, Trip.route_id == Route.route_id).group_by(Route.route_short_name).all()
    
    return jsonify([{'name': stat[0], 'count': stat[1]} for stat in stats])