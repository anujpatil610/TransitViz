from flask import render_template, abort
from app import app
from app.utils.gtfs_parser import load_gtfs_file

@app.route('/')
def index():
    return render_template('index.html', title='Home')

from flask import render_template
from app import app
from app.utils.gtfs_parser import load_gtfs_file

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    # Load the GTFS data after ensuring the files are extracted
    try:
        routes = load_gtfs_file('routes.txt')
        return render_template('gtfs_dashboard.html', routes=routes)
    except FileNotFoundError:
        return "GTFS data file not found", 500
    except Exception as e:
        return f"An error occurred: {e}", 500


@app.route('/gps-dashboard')
def gps_dashboard():
    # Placeholder content for now
    return render_template('gps_dashboard.html', title='GPS Dashboard')
