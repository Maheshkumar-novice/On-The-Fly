from flask import redirect, render_template, request, url_for
from sqlalchemy import select

from application import db
from application.auth.models import User
from application.business.models import BusinessInformation
from application.customer.forms import BusinessSearchForm


def home():
    return redirect(url_for('customer.feed'))


def feed():
    form = BusinessSearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        return redirect(url_for('customer.feed', search=search_term))

    search_term = request.args.get('search')
    if search_term:
        query = select(User, BusinessInformation) \
            .join(BusinessInformation) \
            .filter(User.role_id == 1,
                    User.name.ilike(f'%{search_term}%',
                                    User.id == BusinessInformation.user_id))
        businesses = [{**business.to_dict(), **business_information.to_dict()}
                      for business, business_information in db.session.execute(query).all()]
    else:
        query = select(User, BusinessInformation) \
            .join(BusinessInformation) \
            .filter(User.role_id == 1,
                    BusinessInformation.user_id == User.id)
        businesses = [{**business.to_dict(), **business_information.to_dict()}
                      for business, business_information in db.session.execute(query).all()]

    form.search_term.default = search_term
    form.process()

    return render_template('customer_feed.html', navbar_type='user', user_type='customer', businesses=businesses, form=form)
