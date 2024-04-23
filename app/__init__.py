from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+os.getenv('DB_USER', 'postgres')+':'+os.getenv('DB_PASS', '<your_default_password>')+'@'+os.getenv('DB_HOST', 'localhost')+':'+os.getenv('DB_PORT', '5432')+'/'+os.getenv('DB_NAME', 'gtfs')


# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Import routes from the routes module
from app import routes
