import base64
from flask import Flask
from app.routes import initialize_routes  # Import your route initialization function if applicable

def create_app():
    app = Flask(__name__)

    # Initialize your routes
    initialize_routes(app)

    # Define and register the custom filter
    def b64encode(data):
        """Encode binary data to a base64 string."""
        return base64.b64encode(data).decode('utf-8')

    # Register the filter with Jinja2
    app.jinja_env.filters['b64encode'] = b64encode

    return app
