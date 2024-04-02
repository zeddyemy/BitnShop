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


from .models import *
from .extensions import db, admin, migrate, cors, login_manager
#from .utils.middleware import set_access_control_allows
from .config import Config, configure_logging, config_by_name
from .context_processors import my_context_Processor

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
    app.config.update(
        SERVER_NAME='localhost:2001',
        APPLICATION_ROOT='/',
        PREFERRED_URL_SCHEME='http'
    )
    app.context_processor(my_context_Processor)

    # Initialize Flask extensions here
    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app)
    cors.init_app(app) # Set up CORS. Allow '*' for origins.
    
    #Login Configuration
    login_manager.init_app(app)
    login_manager.login_view = 'front.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return AppUser.query.get(int(user_id))

    
    add_admin_views()
    
    # Use the after_request decorator to set Access-Control-Allow
    #app.after_request(set_access_control_allows)
    
    #app.before_request(ping_url)
    # app.before_request(json_check)
    
    
    # Configure logging
    configure_logging(app)
    
    
    # Register blueprints
    from .core.routes.front import front_bp
    app.register_blueprint(front_bp)
    
    from .core.routes.panel import panel_bp
    app.register_blueprint(panel_bp)
    
    with app.app_context():
        create_roles()  # Create roles for BitnShop
        create_nav_items(True)
    
    return app
