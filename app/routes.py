from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    # Assume data loading functions are defined and called here
    return render_template('gtfs_dashboard.html', title='GTFS Dashboard')

@app.route('/gps-dashboard')
def gps_dashboard():
    # Placeholder content for now
    return render_template('gps_dashboard.html', title='GPS Dashboard')
