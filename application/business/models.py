from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

from application import db
from application.business.constants import TICKET_STATUS_ENUM


class BusinessInformation(db.Model, SerializerMixin):
    __tablename__ = 'business_information'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    business_subtype_id = Column(Integer, ForeignKey(
        'business_subtypes.id'), nullable=False)
    description = Column(String(400), nullable=True)
    gst_no = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    user = relationship('User', back_populates='business_information')
    business_subtype = relationship(
        'BusinessSubType', back_populates='business_information')

    serialize_only = ('description', 'gst_no', 'business_subtype')


class BusinessType(db.Model, SerializerMixin):
    __tablename__ = 'business_types'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    name = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    business_subtypes = relationship(
        'BusinessSubType', cascade='all, delete', back_populates='business_type')

    serialize_only = ('name')


class BusinessSubType(db.Model, SerializerMixin):
    __tablename__ = 'business_subtypes'

    id = Column(Integer, primary_key=True,
                nullable=False, autoincrement=True)
    business_type_id = Column(Integer, ForeignKey(
        'business_types.id'), nullable=False)
    name = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    business_type = relationship(
        'BusinessType', back_populates='business_subtypes')
    business_information = relationship(
        'BusinessInformation', cascade='all, delete', back_populates='business_subtype')

    serialize_only = ('name', 'business_type.name')


class BusinessItem(db.Model, SerializerMixin):
    __tablename__ = 'business_items'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    user = relationship('User', back_populates='business_items')

    serialize_only = ('id', 'name', 'description', 'price',
                      'is_available', 'updated_at')

    @staticmethod
    def convert_price_to_paisas(price):
        return price * 100

    @staticmethod
    def convert_price_to_rupees(price):
        return price / 100


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status = Column(Enum(*TICKET_STATUS_ENUM))
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_for = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    business = relationship(
        'User', back_populates='business_tickets', foreign_keys=[created_for])
    customer = relationship(
        'User', back_populates='customer_tickets', foreign_keys=[created_by])
    ticket_items = relationship('TicketItem', cascade='all, delete')
    ticket_comments = relationship('TicketComment', cascade='all, delete')


class TicketItem(db.Model):
    __tablename__ = 'ticket_items'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    item_name = Column(String(100), nullable=False)
    item_requirement = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    ticket = relationship('Ticket', back_populates='ticket_items')


class TicketComment(db.Model):
    __tablename__ = 'ticket_comments'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    posted_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.now, onupdate=datetime.now)
    ticket = relationship('Ticket', back_populates='ticket_comments')
    user = relationship('User', back_populates='ticket_comments')
