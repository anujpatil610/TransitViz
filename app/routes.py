from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
# Initialize Flask application and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import your models and utilities
from app.models import Route, Stop, Trip, Calendar
from app.utils.gtfs_importer import get_all_route_names

@app.route('/')
def index():
    # Fetch all route names for the dropdown menu
    route_names = get_all_route_names()
    return render_template('index.html', title='Home', route_names=route_names)

@app.route('/timetable', methods=['GET'])
def timetable():
    selected_route_name = request.args.get('route_name')
    route_names = [route.route_long_name for route in Route.query.distinct(Route.route_long_name).all()]
    timetable_html = ""

    if selected_route_name:
        # Fetch trips that are associated with the selected route name
        trips = Trip.query.join(Route).filter(Route.route_long_name == selected_route_name).all()
        if trips:
            # Build a DataFrame for displaying in the timetable
            trips_data = [{'trip_id': trip.trip_id, 'route_name': trip.route.route_long_name} for trip in trips]
            trips_df = pd.DataFrame(trips_data)
            timetable_html = trips_df.to_html(index=False, classes='table table-responsive')
        else:
            timetable_html = "<div class='alert alert-warning'>No trips available for this route.</div>"
    else:
        timetable_html = "<div class='alert alert-info'>Please select a route to view the timetable.</div>"

    return render_template('timetable.html', timetable_html=timetable_html, route_names=route_names)

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    routes = [route.route_long_name for route in Route.query.all()]
    stops = [stop.stop_name for stop in Stop.query.all()]
    return render_template('gtfs_dashboard.html', routes_html=routes, stops_html=stops)

@app.route('/gps-dashboard')
def gps_dashboard():
    return render_template('gps_dashboard.html', title='GPS Dashboard')
