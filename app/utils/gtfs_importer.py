# gtfs_importer.py
from app.models import Route, db

def get_all_route_names():
    route_names = Route.query.with_entities(Route.route_long_name).distinct().all()
    return [name[0] for name in route_names]
