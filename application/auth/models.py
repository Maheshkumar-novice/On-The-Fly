from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from application import db
from application.auth.constants import USER_ROLES_ENUM


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    name = Column(String(75), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mobile_no = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(150), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    role = relationship('Role', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    role_name = Column(Enum(*USER_ROLES_ENUM), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    users = relationship(
        'User', cascade='all, delete', back_populates='role')
