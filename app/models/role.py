from enum import Enum

from ..extensions import db

class RoleNames(Enum):
    """ENUMS for the name filed in Role Model"""
    SUPER_ADMIN = 'Super Admin'
    Admin = 'Admin'
    JUNIOR_ADMIN = 'Junior Admin'
    MODERATOR = 'Moderator'
    CUSTOMER = 'Customer'
    
    @classmethod
    def get_member_by_value(cls, value):
        return next((member for name, member in cls.__members__.items() if member.value == value), None)

# Association table for the many-to-many relationship
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('app_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

# Role data model
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleNames), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
