from lib.mailer import check_verification_token
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, TelField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Regexp,
                                ValidationError)

from application.auth.models import User


class UserRegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], description='Name')
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    mobile_no = TelField('Mobile No', validators=[DataRequired(), Length(
        min=10, max=10), Regexp(regex='^\d{10}$')], description='Mobile No')
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=50), Regexp(regex='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,50}')], description='Password')
    repeat_password = PasswordField('Repeat Password', validators=[
                                    DataRequired(), Length(min=6, max=50), EqualTo('password'), Regexp(regex='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,50}')], description='Repeat Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_mobile_no(self, mobile_no):
        user = User.query.filter_by(mobile_no=mobile_no.data).first()
        if user is not None:
            raise ValidationError('Please use a different mobile number.')


class UserLoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=50), Regexp(regex='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,50}')], description='Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('User not exist.')


class EmailVerificationForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(), Email()], description='Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email not exist.')


class EmailVerificationCodeForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired(), Length(
        min=6, max=6), Regexp(regex='^\d{6}$')], description='Verification Code')

    def validate_code(self, code):
        if not check_verification_token(code.data):
            raise ValidationError('Incorrect Verification Code.')
