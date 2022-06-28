from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import ssl
from application.constants import SECRET

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datum.sqlite3'
    app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET

    ssl._create_default_https_context = ssl._create_unverified_context

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app