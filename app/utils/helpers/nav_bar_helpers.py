"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""
from sqlalchemy import asc

from ...extensions import db
from ...models import NavigationBarItem
from .basic_helpers import console_log

def get_all_nav_items() -> object:
    ''' Gets all Navigation Item rows from database
    '''
    nav_items = NavigationBarItem.query.order_by(asc('order'))
    
    return nav_items