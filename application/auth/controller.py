from flask import redirect, render_template, url_for

from application import db
from application.auth.constants import BUSINESS_ROLE, CUSTOMER_ROLE
from application.auth.forms import UserRegistrationForm
from application.auth.models import Role, User


def get_business_signup_page():
    return render_template('business_signup.html', form=UserRegistrationForm())


def create_business_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'mobile_no': form.mobile_no.data,
            'role_id': Role.query.filter_by(role_name=BUSINESS_ROLE).first().id
        }
        user = User(**user_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('business_signup.html', form=form)

def get_customer_signup_page():
    return render_template('customer_signup.html', form=UserRegistrationForm())


def create_customer_user():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'mobile_no': form.mobile_no.data,
            'role_id': Role.query.filter_by(role_name=CUSTOMER_ROLE).first().id
        }
        user = User(**user_data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('customer_signup.html', form=form)
