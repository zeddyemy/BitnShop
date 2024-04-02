import sys
from urllib.parse import urlparse
from slugify import slugify
from flask import render_template, request, Response, flash, redirect, url_for, abort
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from . import front_bp
from ....extensions import db
from ....models import AppUser, Profile, Address, Role, RoleNames
from ....utils.helpers import get_app_user, log_exception, console_log, redirect_url
from ....utils.forms import SignUpForm, LoginForm


## Route to sign up user
@front_bp.route("/signup", methods=['GET', 'POST'])
def sign_up():
    error = False
    form = SignUpForm()
    
    if current_user.is_authenticated:
        return redirect(redirect_url('front.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print('------ {0}'.format(request.form))
            try:
                username = form.username.data
                email = form.email.data
                firstname = form.firstname.data
                lastname = form.lastname.data
                slug = slugify(username)
                password = form.password.data
                hashed_pwd = generate_password_hash(password, "pbkdf2:sha256")
                
                
                new_user = AppUser(username=username, email=email, thePassword=hashed_pwd)
                new_user_profile = Profile(firstname=firstname, lastname=lastname, app_user=new_user)
                new_user_address = Address(app_user=new_user)
            
                role = Role.query.filter_by(name=RoleNames.CUSTOMER).first()
                if role:
                    new_user.roles.append(role)
                    
                db.session.add_all([new_user, new_user_profile, new_user_address])
                db.session.commit()
            except InvalidRequestError:
                db.session.rollback()
                flash(f"Something went wrong!", "danger")
            except IntegrityError:
                db.session.rollback()
                flash(f"User already exists!.", "warning")
            except (DataError, DatabaseError) as e:
                db.session.rollback()
                log_exception('Database error occurred during registration', e)
                flash(f"Error interacting with the database.", "danger")
            except Exception as e:
                error = True
                errMsg = e
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            
            if error:
                # on unsuccessful db insert, flash an error instead.
                console_log('There was an error', errMsg)
                abort(500)
            else:
                # on successful db insert, flash success
                flash('Your account has been successfully created', 'success')
                return redirect(redirect_url('front.login'))
        else:
            all_fields = ['email', 'username', 'password', 'confirmPasswd']
            if any(field in form.errors for field in all_fields):
                pass
            else:
                for field_name, error_messages in form.errors.items():
                    for err in error_messages:
                        if field_name == "csrf_token":
                            the_err_msg = "Sorry, we could not create your account. Please Try Again."
                            flash(the_err_msg, 'error')
                            console_log(data=err)
                            break
                        
    return render_template('front/auth/register.html', form=form, page='auth')

## Route to Login
@front_bp.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    form = LoginForm()
    
    if current_user.is_authenticated:
        return redirect(redirect_url('front.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            console_log('Form', data=request.form)
            email_username = form.email_username.data
            pwd = form.pwd.data
            
            # get user from db with the email/username.
            user = get_app_user(email_username)
            
            # get next argument fro url
            next = request.args.get('next')
            if not next or urlparse(next).netloc != '':
                next = url_for('front.index')
            
            
            if not user:
                flash("Email/Username is incorrect or doesn't exist", 'error')
                return render_template('front/auth/login.html', form=form, page='auth')
            
            if not user.verify_password(pwd):
                flash("Password is incorrect", 'error')
                return render_template('front/auth/login.html', form=form, page='auth')
            
            login_user(user)
            flash("Welcome back " + user.username, 'success')
            return redirect(next)
            
        else:
            console_log('form.errors', form.errors)
            flash("Something went Wrong. Please Try Again.", 'error')
    
    return render_template('front/auth/login.html', form=form, page='auth')

## Route to Logout
@front_bp.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out", 'success')
    return redirect(url_for('front.login'))

## route to add the admin user
@front_bp.route("/administrator", methods=['GET'])
def admin():
    error = False
    try:
        allRoles = Role.query.all()
        if len(allRoles) < 1:
            # Create all roles for the store
            administrator = Role(name='administrator')
            editor = Role(name='editor')
            trader = Role(name='trader')
            customer = Role(name='customer')
            db.session.add_all([administrator, editor, trader, customer])
            # db.session.add(Role)
            db.session.commit()
    
        # Create 'AdminUser' with 'administrator' roles
        adminRole = Role.query.filter(Role.name=='administrator').first()
        adminRoleId = adminRole.id
        adminUser = AppUser.query.filter(AppUser.role_id==adminRoleId).first()
        
        print("\n-------->>\n", adminUser, "\n<<---------\n\n")
        
        if adminUser:
            flash('please login to access the Control Panel', 'info')
            return redirect(redirect_url('front.login'))
        if not adminUser:
            hashedPw = generate_password_hash('root', "sha256")
            theAdminUser = AppUser(username='admin', email='AdminUser@mail.com', thePassword=hashedPw, role_id=adminRoleId, slug = slugify('admin'))
            theAdminUserProfile = Profile(firstname='Admin', app_user=theAdminUser)
            theAdminUserAddress = Address(defaultAddress='', app_user=theAdminUser)
            
            db.session.add_all([theAdminUser, theAdminUserProfile, theAdminUserAddress])
            db.session.commit()
    except Exception as e:
        error = True
        errMsg = e
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        # on unsuccessful db insert, flash an error instead.
        print("\n----------------->\n There was an error: ", errMsg, "\n<---------------\n" )
        abort(500)
    else:
        adminUser = AppUser.query.filter(AppUser.role_id==adminRoleId).first()
        login_user(adminUser)
        # on successful db insert, flash success
        flash('Welcome to your Dashboard. You can oversea everything on your site from here', 'success')
    
    return redirect(redirect_url('front.index'))

