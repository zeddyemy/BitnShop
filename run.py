'''
This is the entry point of the BitnShop Flask application.

It creates an instance of the application and runs it.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
'''
from app import create_app

app = create_app()