from datetime import datetime
from time import time

import jwt
import pyotp
from flask import url_for
from flask_login import UserMixin
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

    twilio_mail_client = Client(
        Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    sendgrid_mail_client = SendGridAPIClient(Config.SENDGRID_API_KEY)

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

    def send_password_reset_mail(self):
        token = self._get_password_reset_token()
        url = url_for('auth.password_reset', token=token, _external=True)
        message = Mail(
            from_email=Config.SENDGRID_SENDER_EMAIL,
            to_emails=self.email
        )
        message.dynamic_template_data = {
            'password_reset_link': url
        }
        message.template_id = Config.SENDGRID_PASSWORD_RESET_TEMPLATE_ID
        self.sendgrid_mail_client.send(message)

    def is_eligible_for_password_reset(self):
        return self._is_time_limit_reached(self.last_password_reset_sent_at)

    def is_eligible_for_email_verification(self):
        return self._is_time_limit_reached(self.last_email_verification_sent_at)

    def is_eligible_for_mobile_verification(self):
        return self._is_time_limit_reached(self.last_mobile_verification_sent_at)

    def get_remaining_time_for_next_password_reset(self):
        return self._get_remaining_time_to_reach_limit(self.last_password_reset_sent_at)

    def get_remaining_time_for_next_email_verification(self):
        return self._get_remaining_time_to_reach_limit(self.last_email_verification_sent_at)

    def get_remaining_time_for_next_mobile_verification(self):
        return self._get_remaining_time_to_reach_limit(self.last_mobile_verification_sent_at)

    def _send_verification(self, to, type):
        self.twilio_mail_client.verify \
            .services(Config.TWILIO_VERIFY_SERVICE) \
            .verifications \
            .create(to=to, channel=type)

    def _check_verification_token(self, to, token):
        check = self.twilio_mail_client.verify \
            .services(Config.TWILIO_VERIFY_SERVICE) \
            .verification_checks \
            .create(to=to, code=token)
        return check.status == 'approved'

    def _get_password_reset_token(self):
        return jwt.encode({'id': self.id,
                           'exp': time() + Config.JWT_VALIDITY_FOR_PASSWORD_RESET_IN_SECONDS},
                          key=Config.SECRET_KEY,
                          algorithm='HS256')

    def _is_time_limit_reached(self, stored_time):
        time_limit = Config.TIME_LIMIT_NEEDED_FOR_RESEND
        if (not stored_time) or (self._get_time_passed_since(stored_time) > time_limit):
            return True
        return False

    def _get_remaining_time_to_reach_limit(self, stored_time):
        time_limit = Config.TIME_LIMIT_NEEDED_FOR_RESEND
        if not stored_time:
            return 0

        time_passed = self._get_time_passed_since(stored_time)
        remaining_time = time_limit - time_passed

        if remaining_time < 0:
            return 0

        return remaining_time

    def _get_time_passed_since(self, timestamp):
        return (datetime.now() - timestamp).total_seconds()

    @staticmethod
    def create_from_password_reset_token(token):
        try:
            id = jwt.decode(token, key=Config.SECRET_KEY,
                            algorithms=['HS256'])['id']
        except Exception as e:
            print(e)
            return None
        return User.query.filter_by(id=id).first()


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
