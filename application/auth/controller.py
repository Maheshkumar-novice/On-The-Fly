from io import BytesIO

import pyotp
import pyqrcode
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from application import db
from application.auth.constants import BUSINESS_ROLE, CUSTOMER_ROLE
from application.auth.forms import *
from application.auth.models import Role, User


def signup():
    form = UserRegistrationForm()
    account_type = request.args.get('account_type', '')

    if account_type not in [BUSINESS_ROLE, CUSTOMER_ROLE]:
        flash('Invalid Account Type.', category='error')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'mobile_no': f'+91{form.mobile_no.data}',
            'role_id': Role.query.filter_by(role_name=account_type).first().id
        }
        user = User(**user_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login', account_type=account_type))
    return render_template('signup.html', form=form, account_type=account_type)


def login():
    form = UserLoginForm()
    account_type = request.args.get('account_type', '')

    if account_type not in [BUSINESS_ROLE, CUSTOMER_ROLE]:
        flash('Invalid Account Type.', category='error')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        user_validity = user \
            and (user.role.role_name == account_type) \
            and (user.check_password(form.password.data))

        if not user_validity:
            flash('Please check the credentials and try again.', category='error')
            return redirect(url_for('auth.login', account_type=account_type))

        login_user(user)
        return redirect(url_for('auth.security_measures'))
    return render_template('login.html', form=form, account_type=account_type)


@login_required
def security_measures():
    if not current_user.is_email_verified:
        current_user.send_email_verification()
        return redirect(url_for('auth.email_verification'))

    if not current_user.is_mobile_verified:
        current_user.send_mobile_no_verification()
        return redirect(url_for('auth.mobile_verification'))

    if not current_user.is_totp_enabled:
        return redirect(url_for('auth.totp_setup'))

    return redirect(url_for('auth.totp_verification'))


@login_required
def email_verification():
    if current_user.is_email_verified:
        return redirect(url_for('auth.security_measures'))

    form = EmailVerificationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.is_email_verified = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.security_measures'))
    return render_template('verification.html', form=form, template_type='email')


@login_required
def mobile_verification():
    if current_user.is_mobile_verified:
        return redirect(url_for('auth.security_measures'))

    form = MobileVerificationForm()

    if form.validate_on_submit():
        user = User.query.filter_by(mobile_no=current_user.mobile_no).first()
        user.is_mobile_verified = True
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.security_measures'))
    return render_template('verification.html', form=form, template_type='mobile')


@login_required
def totp_setup():
    if current_user.is_totp_enabled:
        return redirect(url_for('auth.security_measures'))

    current_user.totp_secret = pyotp.random_base32()
    db.session.add(current_user)
    db.session.commit()
    return render_template('totp_setup.html'), {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@login_required
def totp_qrcode():
    if current_user.is_totp_enabled:
        return redirect(url_for('auth.security_measures'))

    uri = current_user.create_totp_uri()
    stream = BytesIO()
    url = pyqrcode.create(uri)
    url.svg(stream, scale=5)
    return stream.getvalue(), {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@login_required
def totp_verification():
    form = TOTPVerificationForm()

    if form.validate_on_submit():
        if not current_user.is_totp_enabled:
            current_user.is_totp_enabled = True
            db.session.add(current_user)
            db.session.commit()
        flash('Login Success.', category='info')
        return redirect(url_for('home'))

    return render_template('verification.html', form=form, template_type='totp')


def logout():
    session.clear()
    logout_user()
    return redirect(url_for('home'))
