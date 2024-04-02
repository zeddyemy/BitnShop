from flask_login import current_user

from .utils.helpers.category_helpers import get_all_categories
from .utils.helpers.user_helpers import get_app_user_info
from .utils.helpers.nav_bar_helpers import get_all_nav_items
from .extensions import db

def my_context_Processor():
    if current_user.is_authenticated:
        current_user_obj = db.session.merge(current_user)
        db.session.expunge_all() # detach all objects from the session
        user_id = current_user_obj.id
    else:
        user_id = None
    
    user_info = get_app_user_info(user_id)
    all_categories = get_all_categories()
    all_categories = [cat.to_dict() for cat in all_categories]
    nav_items = [nav_item.to_dict() for nav_item in get_all_nav_items()]
    
    db.session.close() # close the session
    
    return {'CURRENT_USER': user_info, 'ALL_CATEGORIES': all_categories, 'NAV_ITEMS': nav_items}