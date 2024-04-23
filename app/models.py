# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.String, nullable=False, unique=True)
    route_long_name = db.Column(db.String, nullable=False)

class Stop(db.Model):
    __tablename__ = 'stops'
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.String, nullable=False, unique=True)
    stop_name = db.Column(db.String, nullable=False)

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.String, nullable=False, unique=True)
    route_id = db.Column(db.String, db.ForeignKey('routes.route_id'))
    service_id = db.Column(db.String)

class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.String, unique=True)
    monday = db.Column(db.String)
    tuesday = db.Column(db.String)
    # Add other days as needed

# Ensure your Flask application is correctly initializing this module in the main app initialization.
