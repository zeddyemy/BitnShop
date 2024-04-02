"""
Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField, ValidationError)
from wtforms.validators import DataRequired, EqualTo, Length, Email, Regexp

from ...models import AppUser


# Sign up Form
class SignUpForm(FlaskForm):
    username = StringField(
        'Username', validators=[
            DataRequired(),
            Length(3, 20, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, " "numbers, dots or underscores",
            )
        ]
    )
    email = EmailField(
        'Email address', validators=[DataRequired(), Email(), Length(1, 64)]
    )
    firstname = StringField(
        'First Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    lastname = StringField(
        'Last Name', validators=[
            DataRequired(),
            Length(3, 50, message="Please provide a valid name"),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Please Make sure you typed your name correctly",
            )
        ]
    )
    
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(4, 72),
            EqualTo('confirmPasswd', message='Passwords Must Match!')
        ]
    )
    confirmPasswd = PasswordField(
        'Confirm Password', validators=[
            DataRequired(),
            Length(4, 72),
            EqualTo('password', message='Passwords Must Match!')
        ]
    )
    
    def validate_email(self, email):
        if AppUser.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered!")

    def validate_username(self, username):
        if AppUser.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken!")

# form for user to login
class LoginForm(FlaskForm):
    email_username = StringField(
        'Email address', validators=[DataRequired(), Length(1, 64)]
    )
    pwd = PasswordField(
        'Password', validators=[
            DataRequired(), Length(min=4, max=72)
        ]
    )
