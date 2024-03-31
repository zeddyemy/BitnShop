"""
Application factory for BitnShop

It sets up and configures the Flask application, initializes various Flask extensions,
sets up CORS, configures logging, registers blueprints and defines additional app-wide settings.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from flask import Flask, request
from flask_moment import Moment
from flask_migrate import Migrate
from flask_cors import CORS


from .models import *
from .extensions import db
#from .utils.middleware import set_access_control_allows, json_check, ping_url
from .config import Config, configure_logging, config_by_name

def create_app(config_name=Config.ENV):
    """
    Creates and configures the Flask application instance.

    Args:
        config_class: The configuration class to use (Defaults to Config).

    Returns:
        The Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Flask extensions here
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/*": {"origins": Config.CLIENT_ORIGINS}}, supports_credentials=True)

    # Use the after_request decorator to set Access-Control-Allow
    #app.after_request(set_access_control_allows)
    
    #app.before_request(ping_url)
    # app.before_request(json_check)
    
    
    # Configure logging
    configure_logging(app)
    
    
    # Register blueprints
    from .core.routes.front import front_bp
    app.register_blueprint(front_bp)
    
    with app.app_context():
        create_roles()  # Create roles for BitnShops
    
    return app
