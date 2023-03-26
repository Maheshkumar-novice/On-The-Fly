from application.business.models import Ticket, TicketItem
from flask_login import current_user
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import select

from application import db
from application.auth.models import User
from application.business.models import BusinessInformation, TicketComment
from application.customer.forms import BusinessSearchForm
from application.business.forms import BusinessTicketCommentForm


@login_required
def home():
    return redirect(url_for('customer.feed'))


@login_required
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


@login_required
def tickets():
    tickets = [ticket.to_dict() for ticket in Ticket.query.filter(
        Ticket.created_by == current_user.id).all()]

    return render_template('customer_tickets.html', navbar_type='user', user_type='customer', tickets=tickets)


@login_required
def ticket(id):
    form = BusinessTicketCommentForm()
    ticket = Ticket.query.filter(Ticket.id == id)

    if ticket:
        ticket = ticket.scalar().to_dict()
        ticket_items = [ticket_item.to_dict() for ticket_item in TicketItem.query.filter(
            TicketItem.ticket_id == id).all()]
        ticket_comments = [ticket_comment.to_dict(
        ) for ticket_comment in TicketComment.query.filter(TicketComment.ticket_id == id).all()]
        return render_template('customer_ticket.html', navbar_type='user', user_type='customer', ticket=ticket, ticket_items=ticket_items, ticket_comments=ticket_comments, form=form)

    return redirect(url_for('customer.tickets'))
