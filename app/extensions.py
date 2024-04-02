'''
This module initializes the extensions used in the BitnShop Flask application.

It sets up SQLAlchemy, Flask-Mail, and Celery with the configurations defined in the Config class.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
'''

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_admin import Admin
from flask_moment import Moment
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager

from .config import Config

db = SQLAlchemy()
mail = Mail()
migrate = Migrate(db=db)
cors = CORS(resources={r"/*": {"origins": Config.CLIENT_ORIGINS}}, supports_credentials=True)
admin = Admin(name='BitnShop Admin', template_mode='bootstrap4')  # Customize name and theme
login_manager = LoginManager()