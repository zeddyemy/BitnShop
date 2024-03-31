"""
This package contains the database models for the Flask application.

It includes models for User, Product, Category, Role, etc. Each model corresponds to a table in the database.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
License: MIT, see LICENSE for more details.
Package: BitnShop
"""

from .media import Media
from .role import Role, create_roles
from .user import AppUser, Profile, Address, TempUser