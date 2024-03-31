"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from flask import render_template

from . import front_bp

@front_bp.route("/", methods=['GET'])
def index():
    return render_template('front/index.html')