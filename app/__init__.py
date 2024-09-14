from flask import Flask
from .extensions import db, bcrypt
from .routes import register_routes
import base64

def create_app():
    app = Flask(__name__)

    # Initialize your routes
    register_routes(app)
    app.config.from_object('config.Config')
    db.init_app(app)
    bcrypt.init_app(app)

    # Define and register the custom filter
    def b64encode(data):
        """Encode binary data to a base64 string."""
        return base64.b64encode(data).decode('utf-8')

    # Register the filter with Jinja2
    app.jinja_env.filters['b64encode'] = b64encode

    return app