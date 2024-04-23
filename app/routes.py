from flask import render_template
from app import app

@app.route('/')
def index():
    # Fetch all route names for the dropdown menu from the database
    
    return render_template('index.html')

@app.route('/gtfs-dashboard')
def gtfs_dashboard():
    # Fetch routes and stops information from the database for the dashboard
    
    return render_template('gtfs_dashboard.html')

@app.route('/gps-dashboard')
def gps_dashboard():
    # This page is not implemented yet and the link is disabled in the template
    return render_template('gps_dashboard.html', title='GPS Dashboard (Coming Soon)')


@app.route('/timetable', methods=['GET'])
def timetable():
    # Obtain the list of all route long names to pass back to the dropdown in case of form re-render
    

    return render_template('timetable.html')
