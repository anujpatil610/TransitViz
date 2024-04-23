# app/models.py
from app import db

class Trip(db.Model):
    __tablename__ = 'trips'
    trip_id = db.Column(db.String(50), primary_key=True)  # Using 'trip_id' as the primary key
    route_id = db.Column(db.String(50), db.ForeignKey('routes.route_id'), nullable=False)
    service_id = db.Column(db.String(50), nullable=False)
    trip_headsign = db.Column(db.String(100))
    direction_id = db.Column(db.Integer)  # Optional
    block_id = db.Column(db.String(50))  # Optional

    # Relationship with Route
    route = db.relationship('Route', backref=db.backref('trips', lazy=True))

class Route(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.String(50), primary_key=True)
    route_short_name = db.Column(db.String(50), nullable=False)
    route_long_name = db.Column(db.String(100), nullable=False)
    route_type = db.Column(db.Integer, nullable=False)
    route_color = db.Column(db.String(6))
    route_text_color = db.Column(db.String(6))

    # Trips relationship defined in Trip

class Stop(db.Model):
    __tablename__ = 'stops'
    stop_id = db.Column(db.String(50), primary_key=True)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_lat = db.Column(db.Float, nullable=True)
    stop_lon = db.Column(db.Float, nullable=True)
    # If stops are related to trips, you may need a many-to-many relationship
