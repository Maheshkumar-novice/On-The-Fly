from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from application import db
from application.auth.constants import USER_ROLES_ENUM


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    name = Column(String(75), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mobile_no = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(150), nullable=False)
    is_email_verified = Column(Boolean, nullable=False, default=False)
    is_mobile_verified = Column(Boolean, nullable=False, default=False)
    is_totp_enabled = Column(Boolean, nullable=False, default=False)
    totp_secret = Column(String(200), nullable=False, default='')
    last_password_reset_sent_at = Column(DateTime, nullable=True)
    last_email_verification_sent_at = Column(DateTime, nullable=True)
    last_mobile_verification_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    role = relationship('Role', back_populates='users')
    email_verification_code = relationship(
        'EmailVerificationCode', cascade='all, delete', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def format_mobile_no(mobile_no):
        return f'+91{mobile_no}'


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


class UserPasswordResetToken(db.Model):
    __tablename__ = 'used_password_reset_tokens'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    token = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class EmailVerificationCode(db.Model):
    __tablename__ = 'email_verification_codes'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    verification_code = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    user = relationship('User', back_populates='email_verification_code')
