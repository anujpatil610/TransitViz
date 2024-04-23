from flask import render_template, jsonify, request
from app import app, db
from app.models import Route, Stop, Trip
from sqlalchemy import func, distinct

@app.route('/')
def index():
    return render_template('index.html')

# app/routes.py or wherever your Flask routes are defined
from flask import render_template, request
from app import app, db
from app.models import Route, Stop, Trip

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    routes = Route.query.all()
    num_routes = len(routes)
    num_stops = Stop.query.count()
    total_trips = Trip.query.count()

    route_id = request.args.get('route_id')
    route_details = {}

    if route_id:
        selected_route = Route.query.get(route_id)
        if selected_route:
            trips = Trip.query.filter_by(route_id=route_id).all()
            stops = Stop.query.join(Trip, Trip.stop_id == Stop.stop_id).filter(Trip.route_id == route_id).distinct().all()
            
            route_details = {
                'selected_route': selected_route.route_long_name,
                'trips': len(trips),
                'stops': len(set([stop.stop_id for stop in stops])),
                # Calculate headways or other metrics as needed
            }

    return render_template('gtfs_dashboard.html', routes=routes, num_routes=num_routes, num_stops=num_stops,
                           total_trips=total_trips, route_details=route_details)



def get_headways(route_id):
    """Calculate headway for each stop on the route."""
    headways = {}
    trips = Trip.query.filter_by(route_id=route_id).order_by(Trip.start_time).all()
    for trip in trips:
        for idx, stop in enumerate(trip.stops):
            if stop.stop_id not in headways:
                headways[stop.stop_id] = []
            if idx > 0:
                previous_stop_time = trip.stops[idx - 1].arrival_time
                current_stop_time = stop.arrival_time
                headway = (current_stop_time - previous_stop_time).total_seconds() / 60
                headways[stop.stop_id].append(headway)
    return headways

@app.route('/api/routes')
def api_routes():
    routes = Route.query.all()
    return jsonify([{'route_id': route.route_id, 'route_long_name': route.route_long_name} for route in routes])

@app.route('/api/stops')
def api_stops():
    stops = Stop.query.all()
    return jsonify([{'stop_id': stop.stop_id, 'stop_name': stop.stop_name, 'lat': stop.stop_lat, 'lon': stop.stop_lon} for stop in stops])

@app.route('/api/routes/stats')
def route_stats():
    stats = db.session.query(
        Route.route_short_name,
        func.count(distinct(Trip.id)).label('trip_count')
    ).join(Trip, Trip.route_id == Route.route_id).group_by(Route.route_short_name).all()
    return jsonify([{'name': stat[0], 'count': stat[1]} for stat in stats])


@app.route('/timetable', methods=['GET'])
def timetable():
    # Obtain the list of all route long names to pass back to the dropdown in case of form re-render
    route_names = [route.route_long_name for route in Route.query.distinct(Route.route_long_name).all()]
    selected_route_name = request.args.get('route_name')
    timetable_html = ""

    if selected_route_name:
        # Query database for trips associated with the selected route
        trips = Trip.query.join(Route).filter(Route.route_long_name == selected_route_name).all()
        if trips:
            # Process trip data into a format suitable for display
            trips_data = [{'trip_id': trip.trip_id, 'route_name': trip.route.route_long_name} for trip in trips]
            timetable_html = render_template('partials/timetable_data.html', trips_data=trips_data)
        else:
            timetable_html = "<div class='alert alert-warning'>No trips available for this route.</div>"
    else:
        timetable_html = "<div class='alert alert-info'>Please select a route to view the timetable.</div>"

    return render_template('timetable.html', timetable_html=timetable_html, route_names=route_names)
