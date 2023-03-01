from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from application import db
from application.business.forms import (BusinessHomePageEditForm,
                                        BusinessItemForm, BusinessItemSearchForm)
from application.business.models import (BusinessInformation, BusinessItem,
                                         BusinessSubType, BusinessType)


@login_required
def home():
    business_information = BusinessInformation.query.filter_by(
        user_id=current_user.id).scalar()
    data = {**current_user.to_dict(), **business_information.to_dict()}
    return render_template('business_home.html', navbar_type='user', user_type='business', business_data=data), {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@login_required
def edit():
    form = BusinessHomePageEditForm()

    business_information = current_user.business_information
    if business_information.business_subtype:
        business_subtype = business_information.business_subtype
        business_type = business_subtype.business_type
        business_type_id = business_type.id
        business_type_choice_default = business_type.name
        business_subtype_choice_default = business_subtype.name
    else:
        business_type_id = 1
        business_type_choice_default = None
        business_subtype_choice_default = None

    business_type_choices = [name for name, in db.session.execute(
        select(BusinessType.name)).all()]
    business_subtype_choices = [name for name, in db.session.execute(
        select(BusinessSubType.name).where(BusinessSubType.business_type_id == business_type_id)).all()]

    form.business_type.choices = business_type_choices
    form.business_subtype.choices = business_subtype_choices
    form.business_type.default = business_type_choice_default
    form.business_subtype.default = business_subtype_choice_default
    form.gst_no.default = business_information.gst_no
    form.description.default = business_information.description

    if request.method == 'POST':
        business_type_id = db.session.execute(select(BusinessType.id).where(
            BusinessType.name == form.business_type.data)).scalar()
        business_subtype_choices = [name for name, in db.session.execute(
            select(BusinessSubType.name).where(BusinessSubType.business_type_id == business_type_id)).all()]
        form.business_subtype.choices = business_subtype_choices

    if form.validate_on_submit():
        business_subtype_name = form.business_subtype.data
        business_subtype_id = db.session.execute(select(BusinessSubType.id).where(
            BusinessSubType.name == business_subtype_name)).scalar()

        business_information = BusinessInformation.query.filter_by(
            user_id=current_user.id).scalar()
        business_information.gst_no = form.gst_no.data
        business_information.description = form.description.data
        business_information.business_subtype_id = business_subtype_id
        db.session.add(business_information)
        db.session.commit()
        return redirect(url_for('business.home'))

    form.process()

    return render_template('business_home_edit.html', form=form)


@login_required
def business_subtypes():
    business_type_name = request.args.get('type')

    if business_type_name:
        business_type = BusinessType.query.filter_by(
            name=business_type_name).scalar()

        if not business_type:
            return []

        return [business_subtype.to_dict()['name'] for business_subtype in business_type.business_subtypes]

    return []


@login_required
def business_items():
    form = BusinessItemSearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        return redirect(url_for('business.business_items', search=search_term))

    search_term = request.args.get('search')
    if search_term:
        business_items = [business_item.to_dict() for business_item in BusinessItem.query.filter(
            BusinessItem.user_id == current_user.id, BusinessItem.is_available == True, BusinessItem.name.ilike(f'%{search_term}%')).all()]
    else:
        business_items = [business_item.to_dict() for business_item in BusinessItem.query.filter_by(
            user_id=current_user.id, is_available=True).all()]

    return render_template('business_items.html', navbar_type='business_items', user_type='business', business_items=business_items, form=form)


@login_required
def create_business_item():
    form = BusinessItemForm()

    if form.validate_on_submit():
        data = {
            'user_id': current_user.id,
            'name': form.name.data,
            'description': form.description.data,
            'price': form.price.data * 100,
            'is_available': form.is_available.data
        }
        business_item = BusinessItem(**data)
        db.session.add(business_item)
        db.session.commit()
        return redirect(url_for('business.business_items'))

    return render_template('create_business_item.html', navbar_type='user', user_type='business', form=form)
