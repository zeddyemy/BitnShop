'''
This module defines the configuration settings for the BitnShop Flask application.

It includes configurations for the environment, database, mail, and Cloudinary. 
It also includes a function to configure logging for the application.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
'''
import os, logging



class Config:
    # other app configurations
    ENV = os.environ.get('ENV') or 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:zeddy@localhost:5432/bitnshop'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = (ENV == 'development')  # Enable debug mode only in development
    STATIC_DIR = 'app/static'
    UPLOADS_DIR = 'app/static/uploads'
    EMERGENCY_MODE = os.environ.get('EMERGENCY_MODE') or False
    DOMAIN_NAME = os.environ.get('DOMAIN_NAME') or 'https://www.trendit3.com'
    API_DOMAIN_NAME = os.environ.get('API_DOMAIN_NAME') or 'https://api.trendit3.com'
    CLIENT_ORIGINS = os.environ.get('CLIENT_ORIGINS') or 'http://localhost:3000,http://localhost:5173,https://trendit3.vercel.app'
    CLIENT_ORIGINS = [origin.strip() for origin in CLIENT_ORIGINS.split(',')]
    
    # Constants
    TASKS_PER_PAGE = os.environ.get('TASKS_PER_PAGE') or 10
    ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE') or 10
    PAYMENT_TYPES = ['task-creation', 'membership-fee', 'credit-wallet', 'item-upload']
    
    # mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'olowu2018@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'doyi bkzc mcpq cvcv'
    MAIL_DEFAULT_SENDER = ('BitnShop', 'olowu2018@gmail.com')
    
    # Cloudinary configurations
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or "dcozguaw3"
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or "798295575458768"
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or "HwXtPdaC5M1zepKZUriKCYZ9tsI"
    

class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    DEBUG_TOOLBAR = True  # Enable debug toolbar
    EXPOSE_DEBUG_SERVER = False  # Do not expose debugger publicly

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False
    DEBUG_TOOLBAR = False
    EXPOSE_DEBUG_SERVER = False

# Map config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

def configure_logging(app):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)  # Set the desired logging level
