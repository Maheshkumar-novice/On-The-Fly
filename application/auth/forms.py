from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TelField, EmailField
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
