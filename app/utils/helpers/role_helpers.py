"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from sqlalchemy import desc

from ...extensions import db
from ...models import Role
from .basic_helpers import console_log

def get_role_names():
    """returns a list containing the names of all the roles"""
    role_names = []
    
    all_roles = db.session.query(Role.name).order_by(desc('id')).all()
    console_log('getAllRoles', all_roles)
    for role in all_roles:
        role_names.append(role.name.value)
    
    
    return role_names

def get_role_id(role_name):
    role_from_Db = Role.query.filter(Role.name.value == role_name).first()
    customer_role = Role.query.filter(Role.name.value == 'customer').first()
                    
    if role_from_Db:
        role_id = role_from_Db.id
    else:
        role_id = customer_role.id

    return role_id

def admin_roles():
    all_roles = Role.query.filter(Role.name != 'Customer').all()
    admin_roles = [role.name.value for role in all_roles]
    
    return admin_roles

def admin_editor_roles():
    all_roles = Role.query.filter(Role.name.in_(['Administrator', 'Editor'])).all()
    admin_editor_roles = [role.name for role in all_roles]
    
    return admin_editor_roles
