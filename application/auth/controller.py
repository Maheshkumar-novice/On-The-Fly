from datetime import datetime
from io import BytesIO
from random import randint
from time import time

import jwt
import pyotp
import pyqrcode
from flask import (current_app, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from application import db
from application.auth.constants import BUSINESS_ROLE, CUSTOMER_ROLE
from application.auth.forms import *
from application.auth.models import *
from application.business.models import BusinessInformation
from lib.external_services import (get_totp_uri, send_mobile_no_verification,
                                   send_password_reset_mail,
                                   send_verification_mail)
from lib.time_utils import (get_remaining_time_to_reach_eligibility,
                            is_eligible_for_retry)


def signup():
    if not current_user.is_anonymous:
        return redirect(url_for('auth.user_home'))

    form = UserRegistrationForm()
    account_type = request.args.get('account_type', '')

    if account_type not in [BUSINESS_ROLE, CUSTOMER_ROLE]:
        flash('Invalid Account Type.', category='error')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'mobile_no': User.format_mobile_no(form.mobile_no.data),
            'role_id': Role.query.filter_by(role_name=account_type).first().id
        }
        user = User(**user_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        if account_type == BUSINESS_ROLE:
            db.session.add(BusinessInformation(user_id=user.id))
            db.session.commit()

        return redirect(url_for('auth.login', account_type=account_type))
    return render_template('signup.html', form=form, account_type=account_type)


def login():
    if not current_user.is_anonymous:
        return redirect(url_for('auth.user_home'))

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
        if is_eligible_for_retry(current_user.last_email_verification_sent_at):
            current_user.last_email_verification_sent_at = datetime.now()
            db.session.add(current_user)
            db.session.commit()

            verification_code = pyotp.otp.OTP(
                pyotp.random_base32()).generate_otp(randint(1, 100000))

            if current_user.email_verification_code:
                email_verification_code = current_user.email_verification_code
                current_user.email_verification_code.verification_code = verification_code
            else:
                email_verification_code = EmailVerificationCode(
                    user_id=current_user.id, verification_code=verification_code)

            db.session.add(email_verification_code)
            db.session.commit()

            send_verification_mail(current_user.email, verification_code)

            flash(
                'Please check your mail to get the code. You can also try again using Get Code Again, if needed.', category='info')
        else:
            flash(get_remaining_time_to_reach_eligibility(
                current_user.last_email_verification_sent_at), category='timer')
        return redirect(url_for('auth.email_verification'))

    if not current_user.is_mobile_verified:
        if is_eligible_for_retry(current_user.last_mobile_verification_sent_at):
            current_user.last_mobile_verification_sent_at = datetime.now()
            db.session.add(current_user)
            db.session.commit()

            send_mobile_no_verification(current_user.mobile_no)

            flash(
                'Please check your mobile to get the code. You can also try again using Get Code Again, if needed.', category='info')
        else:
            flash(get_remaining_time_to_reach_eligibility(
                current_user.last_mobile_verification_sent_at), category='timer')
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

    uri = get_totp_uri(current_user.email, current_user.totp_secret)
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
        return redirect(url_for('auth.user_home'))

    return render_template('verification.html', form=form, template_type='totp')


def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if is_eligible_for_retry(user.last_password_reset_sent_at):
            user.last_password_reset_sent_at = datetime.now()
            db.session.add(user)
            db.session.commit()

            token = jwt.encode({'id': user.id,
                                'exp': time() + current_app.config['JWT_VALIDITY_FOR_PASSWORD_RESET_IN_SECONDS']},
                               key=current_app.config['SECRET_KEY'],
                               algorithm='HS256')
            url = url_for('auth.password_reset', token=token, _external=True)
            send_password_reset_mail(user.email, url)

            flash(
                'Please check your mail to reset your password. You can also try again by filling the form, if needed.', category='info')
            return redirect(url_for('auth.forgot_password'))

        flash(get_remaining_time_to_reach_eligibility(
            user.last_password_reset_sent_at), category='timer')
        return redirect(url_for('auth.forgot_password'))

    return render_template('forgot_password.html', form=form)


def password_reset(token):
    if UserPasswordResetToken.query.filter_by(token=token).first():
        flash('Token is already used. Please try again.', category='error')
        return redirect(url_for('auth.forgot_password'))

    try:
        id = jwt.decode(token, key=current_app.config['SECRET_KEY'],
                        algorithms=['HS256'])['id']
    except Exception as e:
        print(e)
        id = None

    user = User.query.filter_by(id=id).first()
    if not user:
        flash(
            'Either the token is expired or invalid for password reset. Please try again.',
            category='error')
        return redirect(url_for('auth.forgot_password'))

    form = PasswordResetForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.add(UserPasswordResetToken(token=token))
        db.session.commit()
        flash('Password reset success.', category='info')
        return redirect(url_for('home'))

    return render_template('password_reset.html', form=form, token=token)


def logout():
    session.clear()
    logout_user()
    flash('User Logged out.', category='info')
    return redirect(url_for('home'))


@login_required
def user_home():
    user_role = Role.query.filter_by(id=current_user.role_id).scalar()

    if user_role.role_name == BUSINESS_ROLE:
        return redirect(url_for('business.home'))

    return redirect(url_for('customer.home'))
