from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from application import db
from sqlalchemy_serializer import SerializerMixin


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
    user = relationship('User')
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