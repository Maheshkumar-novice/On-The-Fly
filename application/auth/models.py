from datetime import datetime

import pyotp
from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from twilio.rest import Client
from werkzeug.security import check_password_hash, generate_password_hash

from application import db
from application.auth.constants import USER_ROLES_ENUM
from config import Config


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    mail_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

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
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    role = relationship('Role', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def send_email_verification(self):
        self._send_verification(self.email, type='email')

    def send_mobile_no_verification(self):
        self._send_verification(self.mobile_no, type='sms')

    def check_email_verification_token(self, token):
        return self._check_verification_token(self.email, token)

    def check_mobile_no_verification_token(self, token):
        return self._check_verification_token(self.mobile_no, token)

    def create_totp_uri(self):
        return pyotp.totp.TOTP(self.totp_secret).provisioning_uri(
            issuer_name='On The Fly', name=self.email)

    def check_totp(self, totp):
        return pyotp.TOTP(self.totp_secret).now() == totp

    def _send_verification(self, to, type):
        self.mail_client.verify \
            .services(Config.TWILIO_VERIFY_SERVICE) \
            .verifications \
            .create(to=to, channel=type)

    def _check_verification_token(self, to, token):
        check = self.mail_client.verify \
            .services(Config.TWILIO_VERIFY_SERVICE) \
            .verification_checks \
            .create(to=to, code=token)
        return check.status == 'approved'


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
