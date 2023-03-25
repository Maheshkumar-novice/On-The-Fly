from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from application import db
from application.auth.models import User
from application.business.constants import NEW
from application.business.forms import (BusinessHomePageEditForm,
                                        BusinessItemEditForm, BusinessItemForm,
                                        BusinessItemSearchForm,
                                        BusinessTicketForm)
from application.business.models import (BusinessInformation, BusinessItem,
                                         BusinessSubType, BusinessType, Ticket,
                                         TicketItem)


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
            BusinessItem.user_id == current_user.id, BusinessItem.name.ilike(f'%{search_term}%')).all()]
    else:
        business_items = [business_item.to_dict() for business_item in BusinessItem.query.filter_by(
            user_id=current_user.id).all()]

    form.search_term.default = search_term
    form.process()

    return render_template('business_items.html', navbar_type='business_items', user_type='business', business_items=business_items, form=form)


@login_required
def create_business_item():
    form = BusinessItemForm()

    if form.validate_on_submit():
        data = {
            'user_id': current_user.id,
            'name': form.name.data,
            'description': form.description.data,
            'price': BusinessItem.convert_price_to_paisas(form.price.data),
            'is_available': form.is_available.data
        }
        business_item = BusinessItem(**data)
        db.session.add(business_item)
        db.session.commit()
        return redirect(url_for('business.business_items'))

    return render_template('create_business_item.html', navbar_type='user', user_type='business', form=form)


@login_required
def edit_business_item():
    try:
        id = int(request.args.get('id'))
    except Exception:
        id = None

    if id:
        business_item = BusinessItem.query.filter_by(id=id).scalar()
    else:
        return redirect(url_for('business.business_items'))

    form = BusinessItemEditForm(id=id)

    if form.validate_on_submit():
        business_item.name = form.name.data
        business_item.description = form.description.data
        business_item.price = BusinessItem.convert_price_to_paisas(
            form.price.data)
        business_item.is_available = form.is_available.data
        db.session.add(business_item)
        db.session.commit()
        return redirect(url_for('business.business_items'))

    form.name.default = business_item.name
    form.description.default = business_item.description
    form.price.default = BusinessItem.convert_price_to_rupees(
        business_item.price)
    form.is_available.default = business_item.is_available

    form.process()

    return render_template('edit_business_item.html', navbar_type='user', user_type='business', business_item=business_item, form=form)


@login_required
def delete_business_item():
    try:
        id = int(request.args.get('id'))
    except Exception:
        id = None

    if id:
        business_item = BusinessItem.query.filter_by(id=id).scalar()
        if business_item:
            db.session.delete(business_item)
            db.session.commit()

        return {'id': id}

    return {'id': -1}, 404


@login_required
def view(id):
    query = select(User, BusinessInformation) \
        .join(BusinessInformation) \
        .filter(User.id == id,
                User.role_id == 1,
                BusinessInformation.user_id == User.id)
    data = [{**business.to_dict(), **business_information.to_dict()}
            for business, business_information in db.session.execute(query).all()][0]

    return render_template('business_view.html', navbar_type='user', user_type='customer', business_data=data)


@login_required
def business_items_view(id):
    form = BusinessItemSearchForm()

    if form.validate_on_submit():
        search_term = form.search_term.data
        return redirect(url_for('business.business_items_view', id=id, search=search_term))

    search_term = request.args.get('search')
    if search_term:
        business_items = [business_item.to_dict() for business_item in BusinessItem.query.filter(
            BusinessItem.user_id == id, BusinessItem.name.ilike(f'%{search_term}%')).all()]
    else:
        business_items = [business_item.to_dict() for business_item in BusinessItem.query.filter_by(
            user_id=id).all()]

    form.search_term.default = search_term
    form.process()

    return render_template('business_items_view.html', navbar_type='business_items_view', user_type='customer', business_items=business_items, form=form, id=id)


@login_required
def ticket(business_id):
    form = BusinessTicketForm()
    return render_template('business_ticket.html', navbar_type='user', user_type='customer', form=form, business_id=business_id)


@login_required
def items_by_business_id(business_id):
    return [business_item.name for business_item in BusinessItem.query.filter_by(user_id=business_id).all()]


@login_required
def create_ticket():
    try:
        business_id = int(request.args.get('id'))
    except Exception:
        return 'Business Not Found', 404

    ticket = Ticket()
    ticket.status = NEW
    ticket.created_by = current_user.id
    ticket.created_for = business_id
    db.session.add(ticket)
    db.session.commit()

    payload = request.get_json()

    for ticket_item_data in payload:
        ticket_item = TicketItem()
        ticket_item.item_name = ticket_item_data['name']
        ticket_item.item_requirement = ticket_item_data['requirement']
        ticket_item.ticket_id = ticket.id
        db.session.add(ticket_item)
        db.session.commit()

    return {}, 200


@login_required
def tickets():
    tickets = [ticket.to_dict() for ticket in Ticket.query.filter(
        Ticket.created_for == current_user.id).all()]

    return render_template('business_tickets.html', navbar_type='user', user_type='business', tickets=tickets)


@login_required
def ticket_by_id(id):
    ticket = Ticket.query.filter(Ticket.id == id)

    if ticket:
        ticket = ticket.scalar().to_dict()
        ticket_items = [ticket_item.to_dict() for ticket_item in TicketItem.query.filter(
            TicketItem.ticket_id == id).all()]
        return render_template('business_ticket_view.html', navbar_type='user', user_type='business', ticket=ticket, ticket_items=ticket_items)

    return redirect(url_for('business.tickets'))
