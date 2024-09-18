from flask import Flask
from .extensions import db, bcrypt, login_manager
from .routes import register_routes
import base64

def create_app():
    app = Flask(__name__)

    # Load the configuration
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Initialize LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Redirect to 'login' page if unauthorized access
    login_manager.login_message_category = 'info'  # Flash message category

    # Register routes
    register_routes(app)

    # Function to encode data in base64 and register as a Jinja2 filter
    def b64encode(data):
        """Encode binary data to a base64 string."""
        return base64.b64encode(data).decode('utf-8')

    # Register the filter with Jinja2
    app.jinja_env.filters['b64encode'] = b64encode

    return app
