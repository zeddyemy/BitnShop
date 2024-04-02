"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from wtforms import Form
from wtforms import StringField

from ..extensions import db, admin
from ..config import Config
from .user import AppUser, Profile
from .category import Category
from ..utils.helpers.basic_helpers import console_log

class AppUserModelView(ModelView):
    # Define form rules for create and edit forms
    form_rules = [
        rules.FieldSet(('username', 'email', 'date_joined'), 'AppUser'),
        rules.FieldSet(('firstname', 'lastname', 'gender', 'phone'), 'Profile')
    ]
    
    form_extra_fields = {
        'firstname': StringField('First Name'),
        'lastname': StringField('Last Name'),
        'gender': StringField('Gender'),
        'phone': StringField('Phone')
    }
    
    # Define columns for the list view
    column_list = ('username', 'email', 'date_joined', 'firstname', 'lastname', 'gender', 'phone')
    
    def on_model_change(self, form, model, is_created):
        # Update the related Profile instance
        if model.profile is not None:
            model.profile.firstname = form.firstname.data
            model.profile.lastname = form.lastname.data
            model.profile.gender = form.gender.data
            model.profile.phone = form.phone.data

    
    def get_list(self, *args, **kwargs):
        # Override to include fields from Profile in the list view
        count, data = super().get_list(*args, **kwargs)
        console_log('count, data', f"{count} \n\n {data}")
        for item in data:
            console_log('item', f"{item}")
            if item.profile is not None:
                item.firstname = item.profile.firstname
                item.lastname = item.profile.lastname
                item.gender = item.profile.gender
                item.phone = item.profile.phone
        return count, data

    def get_one(self, id):
        # Override to include fields from Profile in the details view
        item = super().get_one(id)
        if item.profile is not None:
            item.firstname = item.profile.firstname
            item.lastname = item.profile.lastname
            item.gender = item.profile.gender
            item.phone = item.profile.phone
        return item




class AppUserView(ModelView):
    can_create = True  # Allow creating new Profile records within AppUser view
    can_edit = True  # Allow editing existing Profile records
    can_delete = True  # Allow deleting Profile records
    
    form_args = {
        'firstname': {'label': 'First Name'},  # Customize field labels
        'lastname': {'label': 'Last Name'},
        # ... add more form_args for other fields if needed
    }
    
    form_excluded_columns = ['app_user']  # Exclude the foreign key field


class CategoryModelView(ModelView):
    pass

def add_admin_views() -> None:
    admin.add_view(AppUserModelView(AppUser, db.session))
    admin.add_view(CategoryModelView(Category, db.session))