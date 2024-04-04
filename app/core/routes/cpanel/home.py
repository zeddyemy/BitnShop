"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from flask import render_template
from flask_login import login_required
from ....decorators import cpanel_login_required

from . import cpanel_bp

@cpanel_bp.route("/", methods=['GET'])
@cpanel_login_required()
def index():
    return render_template('cpanel/index.html')