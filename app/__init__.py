from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__)

# Use environment variables directly for configuration or set defaults safely
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
    f"{os.getenv('DB_PASS', 'your_default_password')}"  # Avoid using real passwords as defaults
    f"@{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '5432')}/"
    f"{os.getenv('DB_NAME', 'gtfs')}"
)

# It is a good practice to set SQLALCHEMY_TRACK_MODIFICATIONS to False to disable feature that consumes memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Ensure routes are imported after the Flask app has been created and configured
from app import routes
