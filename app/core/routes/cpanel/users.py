"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from slugify import slugify
from flask import request, render_template, flash, redirect, url_for
from sqlalchemy.exc import ( InvalidRequestError, IntegrityError, DataError, DatabaseError )
from werkzeug.security import generate_password_hash

from . import cpanel_bp
from ....models import AppUser, Profile, Address, Role, RoleNames
from ....extensions import db
from ....utils.helpers import console_log, log_exception, redirect_url
from ....decorators import cpanel_login_required
from ....utils.forms import AdminAddUserForm

@cpanel_bp.route("/users", methods=['GET'])
@cpanel_login_required()
def users():
    page = request.args.get("page", 1, type=int)
    all_users = AppUser.query.options(db.joinedload(AppUser.roles), db.joinedload(AppUser.profile), db.joinedload(AppUser.address))
    
    pagination = all_users.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('cpanel/users/users.html', all_users=pagination)


@cpanel_bp.route("/users/new", methods=['GET', 'POST'])
@cpanel_login_required()
def add_new_User():
    form = AdminAddUserForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            console_log('form', request.form)
            try:
                username = form.username.data
                email = form.email.data
                firstname = form.firstname.data
                lastname = form.lastname.data
                password = form.password.data
                slug = slugify(username)
                role = form.role.data
                hashed_pwd = generate_password_hash(password, "pbkdf2:sha256")
                
                new_user = AppUser(username=username, email=email, thePassword=hashed_pwd)
                new_user_profile = Profile(firstname=firstname, lastname=lastname, app_user=new_user)
                new_user_address = Address(app_user=new_user)
                
                # get role from db where the name is same as form role
                user_role = Role.query.filter(Role.name == RoleNames.get_member_by_value(role)).first()
                if user_role:
                    new_user.roles.append(user_role)
            
                db.session.add_all([new_user, new_user_profile, new_user_address])
                db.session.commit()
                
                # on successful db insert, flash success
                flash("New users has been successfully added. Login details will be sent to user's Email", 'success')
                console_log('redirect', url_for('cpanel.users'))
                return redirect(url_for('cpanel.users'))
            except ValueError as e:
                db.session.rollback()
                log_exception('Value error occurred while adding user', e)
                flash(f"An unexpected error occurred!", "danger")
            except InvalidRequestError:
                db.session.rollback()
                flash(f"An unexpected error occurred!", "danger")
            except IntegrityError:
                db.session.rollback()
                flash(f"User already exists!.", "warning")
            except (DataError, DatabaseError) as e:
                db.session.rollback()
                log_exception('Database error occurred while adding user', e)
                flash(f"Error interacting with the database.", "danger")
            except Exception as e:
                db.session.rollback()
                flash(f"An unexpected error occurred!", "danger")
                log_exception('An exception occurred while adding user', e)
        else:
            allFields = ['email', 'username', 'password', 'role']
            if any(field in form.errors for field in allFields):
                console_log('form.errors', form.errors)
                pass
            else:
                for fieldName, errorMessages in form.errors.items():
                    for err in errorMessages:
                        if fieldName == "csrf_token":
                            theErrMsg = "Sorry, we could not add the user. Please Try Again."
                            flash(theErrMsg, 'error')
                            console_log('error', err)
                            break
    
    return render_template('cpanel/users/new_user.html', form=form)
