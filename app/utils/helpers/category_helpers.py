"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

import sys
from flask import request, jsonify, current_app
from sqlalchemy import desc

from ...extensions import db
from ...models import Category
from ...config import Config
from .basic_helpers import int_or_none, generate_slug, console_log


def get_category_names():
    categories = db.session.query(Category.name).order_by(desc('id')).all()
    console_log('categories', categories)
    Category_names = []
        
    for cat in categories:
        Category_names.append(cat.name)
        
    return Category_names

def get_all_categories(cat_id: int=None, page_num: int=None, paginate: bool = False) -> object:
    ''' Gets all Category rows from database
    
    This will return a pagination of all Category rows from database.
    :param cat_id: The ID of a Category. if cat_id is passed, it will return the sub categories of the category
    
    Alternatively, you can use get_sub_categories(id) to get the sub categories without pagination
    '''
    
    if not page_num:
        page_num = request.args.get("page", 1, type=int)
    
    if not cat_id:
        all_categories = Category.query.order_by(desc('id'))
    elif cat_id:
        all_categories = Category.query.filter(Category.parent_id == cat_id).all()
    
    if paginate:
        pagination = all_categories.paginate(page=page_num, per_page=RESULTS_PER_PAGE, error_out=False)
        
        RESULTS_PER_PAGE = int('10')
        pagination = all_categories \
            .order_by(Category.id.desc()) \
            .paginate(page=page_num, per_page=RESULTS_PER_PAGE, error_out=False)
        
        return pagination
    
    return all_categories