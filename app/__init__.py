from flask import Flask
from .extensions import db, bcrypt
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    # Configuration setup (from config.py)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)

    # Register routes
    register_routes(app)

    return app
