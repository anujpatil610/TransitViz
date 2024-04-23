# app/models.py
from app import db

class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.String(50), nullable=False, unique=True)
    route_id = db.Column(db.String(50), db.ForeignKey('routes.route_id'), nullable=False)
    service_id = db.Column(db.String(50), nullable=False)
    trip_headsign = db.Column(db.String(100))
    direction_id = db.Column(db.Integer)  # Optional: 0 for one direction, 1 for the opposite direction
    block_id = db.Column(db.String(50))  # Optional: A block represents a set of trips that a vehicle will be assigned to

    # Establish a relationship with the Route model
    route = db.relationship('Route', back_populates='trips')

# Update Route model to include a relationship with Trip
class Route(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.String(50), primary_key=True)
    route_short_name = db.Column(db.String(50), nullable=False)
    route_long_name = db.Column(db.String(100), nullable=False)
    route_type = db.Column(db.Integer, nullable=False)
    route_color = db.Column(db.String(6))
    route_text_color = db.Column(db.String(6))
    
    # Relationship with trips
    trips = db.relationship('Trip', back_populates='route')

class Stop(db.Model):
    __tablename__ = 'stops'
    stop_id = db.Column(db.String(50), primary_key=True)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_lat = db.Column(db.Float, nullable=True)
    stop_lon = db.Column(db.Float, nullable=True)


