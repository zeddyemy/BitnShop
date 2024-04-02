"""
This module defines the `roles_required` decorator for the BitnShop Flask application.

Used for handling role-based access control.
The `roles_required` decorator is used to ensure that the current user has all of the specified roles.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""
from functools import wraps
from flask_login import LoginManager, login_required, current_user
from flask import current_app, request, redirect, flash, url_for, render_template

from ..models import AppUser

def roles_required(*required_roles):
    """
    Decorator to ensure that the current user has all of the specified roles.

    This decorator will return a 403 error if the current user does not have
    all of the roles specified in `required_roles`.

    Args:
        *required_roles (str): The required roles to access the route.

    Returns:
        function: The decorated function.

    Raises:
        HTTPException: A 403 error if the current user does not have the required roles.
    """
    def decorator(fn):
        @wraps(fn)
        @login_required()
        def wrapper(*args, **kwargs):
            current_user_id = current_user.id
            user = AppUser.query.get(current_user_id)
            
            if user and any(role.name.value in required_roles for role in user.roles):
                return fn(*args, **kwargs)
            else:
                return render_template('rs-admin/errors/permission.jinja-html', msg="Access denied: You do not have the required roles to access this resource")
        return wrapper
    return decorator


def cpanel_login_required() -> None:
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            next=request.path
            if not current_user.is_authenticated:
                flash("You need to login first", 'error')
                return redirect(url_for('cpanel.login', next=next))

            return fn(*args, **kwargs)
        return wrapper
    return decorator
