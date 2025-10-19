from flask import Flask
from flask_cors import CORS
from models import db  # SQLAlchemy database object and models
from routes import habit_routes  # Blueprint for habit API endpoints

app = Flask(__name__)

# SQLite database URI, stores data in 'database.db' file within project folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable event system for performance

db.init_app(app)  # Initialize SQLAlchemy with Flask app

CORS(app)  # Enable Cross-Origin Resource Sharing to allow frontend requests

app.register_blueprint(habit_routes)  # Register habits blueprint for API routes

# Within app context, create database tables as defined in models.py if not exist
with app.app_context():
    db.create_all()

# Start Flask dev server when running this file directly
if __name__ == "__main__":
    app.run(debug=True)
