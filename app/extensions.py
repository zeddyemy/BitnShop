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

from .config import Config

db = SQLAlchemy()
mail = Mail()
