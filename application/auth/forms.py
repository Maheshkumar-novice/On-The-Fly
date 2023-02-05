from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, TelField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from application.auth.models import User
from lib.external_services import check_mobile_no_verification_code, check_totp


def password_field(type='password'):
    label = 'Password'
    validators = [
        DataRequired(), Length(min=8, max=50), Regexp(regex='/^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,50}$/')]

    if type == 'repeat_password':
        label = 'Repeat Password'
        validators.append(EqualTo('password'))

    return PasswordField(label, validators=validators, description=label)


class UserRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], description='Name')
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    mobile_no = TelField('Mobile No', validators=[DataRequired(), Length(
        min=10, max=10), Regexp(regex='^\d{10}$')], description='Mobile No')
    password = password_field()
    repeat_password = password_field(type='repeat_password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_mobile_no(self, mobile_no):
        mobile_no = User.format_mobile_no(mobile_no.data)
        user = User.query.filter_by(mobile_no=mobile_no).first()
        if user is not None:
            raise ValidationError('Please use a different mobile number.')


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    password = password_field()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('User not exist.')


class VerificationForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(
        min=6, max=6), Regexp(regex='^\d{6}$')], description='Verification Code')


class EmailVerificationForm(VerificationForm):
    def validate_code(self, code):
        if current_user.email_verification_code.verification_code != code.data:
            raise ValidationError('Incorrect Verification Code.')


class MobileVerificationForm(VerificationForm):
    def validate_code(self, code):
        if not check_mobile_no_verification_code(current_user.mobile_no, code.data):
            raise ValidationError('Incorrect Verification Code.')


class TOTPVerificationForm(VerificationForm):
    def validate_code(self, code):
        if not check_totp(current_user.totp_secret, code.data):
            raise ValidationError('Incorrect Verification Code.')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('User not exist.')


class PasswordResetForm(FlaskForm):
    password = password_field()
    repeat_password = password_field(type='repeat_password')
