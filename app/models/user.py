"""
This module defines the User model for the database.

It includes fields for the user's email, password, and other necessary information,
as well as methods for password hashing and verification.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""
from sqlalchemy.orm import backref
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..extensions import db
from ..models import Media
from ..config import Config


class TempUser(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ID: {self.id}, email: {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'date_joined': self.date_joined,
        }

# Define the User data model.
class AppUser(db.Model, UserMixin):
    __tablename__ = "app_user"
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    thePassword = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    profile = db.relationship('Profile', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    #wallet = db.relationship('Wallet', back_populates="app_user", uselist=False, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'), cascade="all, delete-orphan", single_parent=True)
    #user_settings = db.relationship('UserSettings', back_populates='app_user', uselist=False, cascade='all, delete-orphan')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.thePassword = generate_password_hash(password)
    
    def verify_password(self, password):
        '''
        #This returns True if the password is same as hashed password in the database.
        '''
        return check_password_hash(self.thePassword, password)
    
    @property
    def is_2fa_enabled(self):
        return self.user_settings.is_2fa_enabled
    
    @property
    def wallet_balance(self):
        return self.wallet.balance
    
    @property
    def role_names(self) -> list[str]:
        """Returns a list of role names for the user."""
        return [str(role.name.value) for role in self.roles]
    
    
    def __repr__(self):
        return f'<ID: {self.id}, username: {self.username}, email: {self.email}>'
    
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self) -> dict:
        
        address_info = {}
        if self.address:
            address_info.update({
                'country': self.address.country,
                'state': self.address.state
            })
        
        profile_data = {}
        if self.profile:
            profile_data.update({
                'firstname': self.profile.firstname,
                'lastname': self.profile.lastname,
                'gender': self.profile.gender,
                'phone': self.profile.phone,
                'profile_picture': self.profile.profile_pic,
                'referral_link': self.profile.referral_link,
            })
        
        '''
        user_wallet = self.wallet
        wallet_info = {
            'balance': user_wallet.balance if user_wallet else None,
            'currency_name': user_wallet.currency_name if user_wallet else None,
            'currency_code': user_wallet.currency_code if user_wallet else None,
        }
        '''
        
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_joined': self.date_joined,
            #'wallet': wallet_info,
            'roles': self.role_names,
            **address_info,  # Merge address information into the output dictionary
            **profile_data # Merge profile information into the output dictionary
        }


class Profile(db.Model):
    __tablename__ = "profile"
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(200), nullable=True)
    lastname = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    profile_picture_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False,)
    app_user = db.relationship('AppUser', back_populates="profile")
    
    def __repr__(self):
        return f'<profile ID: {self.id}, name: {self.firstname}>'
    
    @property
    def referral_link(self):
        return f'{Config.DOMAIN_NAME}/signup/{self.app_user.username}'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    @property
    def profile_pic(self):
        if self.profile_picture_id:
            theImage = Media.query.get(self.profile_picture_id)
            if theImage:
                return theImage.get_path()
            else:
                return ''
        else:
            return ''
        
    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'phone': self.phone,
            'profile_picture': self.profile_pic,
            'referral_link': f'{self.referral_link}',
        }


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id', ondelete='CASCADE'), nullable=False,)
    app_user = db.relationship('AppUser', back_populates="address")
    
    def __repr__(self):
        return f'<address ID: {self.id}, country: {self.country}, user ID: {self.user_id}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'state': self.state,
            'user_id': self.user_id
        }

