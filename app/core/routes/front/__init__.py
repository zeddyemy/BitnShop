"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from flask import Blueprint, render_template

front_bp: Blueprint = Blueprint('front', __name__, url_prefix='/')

from . import home, auth