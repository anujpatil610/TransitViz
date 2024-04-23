# app/models.py

from app import db

class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.String(50), nullable=False, unique=True, comment='Unique identifier for a route.')
    agency_id = db.Column(db.String(50), nullable=False, comment='Identifier for the transit agency.')
    route_short_name = db.Column(db.String(50), nullable=False, comment='A short name of a route.')
    route_long_name = db.Column(db.String(100), nullable=False, comment='A long name of a route that describes the route.')
    route_type = db.Column(db.Integer, nullable=False, comment='Type of transportation used on a route.')
    route_color = db.Column(db.String(6), comment='Hexadecimal color code for the route color, e.g., FFFFFF for white.')
    route_text_color = db.Column(db.String(6), comment='Hexadecimal color code for the text color of the route, e.g., 000000 for black.')


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.String(50), unique=True, nullable=False)
    stop_name = db.Column(db.String(100), nullable=False)
    stop_lat = db.Column(db.Float)
    stop_lon = db.Column(db.Float)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.String(50), unique=True, nullable=False)
    route_id = db.Column(db.String(50), db.ForeignKey('route.route_id'), nullable=False)
    service_id = db.Column(db.String(50))
    trip_headsign = db.Column(db.String(100))
