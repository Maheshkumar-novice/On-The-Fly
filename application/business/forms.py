from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, FloatField, SelectField, StringField,
                     TextAreaField)
from wtforms.validators import Length, ValidationError

from application.business.models import (BusinessItem, BusinessSubType,
                                         BusinessType)


class BusinessHomePageEditForm(FlaskForm):
    description = TextAreaField('Description', validators=[
                                Length(min=1, max=400)], description='Description')
    gst_no = StringField('GST No', validators=[
                         Length(min=1, max=100)], description='GST No')
    business_type = SelectField('Business Type', choices=[])
    business_subtype = SelectField('Business SubType', choices=[])

    def validate_business_subtype(self, business_subtype):
        business_type_id_from_chosen_subtype = BusinessSubType.query.filter_by(
            name=business_subtype.data).scalar().business_type_id
        business_type_id_from_input = BusinessType.query.filter_by(
            name=self.business_type.data).scalar().id

        if business_type_id_from_chosen_subtype != business_type_id_from_input:
            raise ValidationError(
                'Please choose the correct business type for this subtype.')


class BusinessItemForm(FlaskForm):
    name = StringField('Name', validators=[
                       Length(min=1, max=100)], description='Name')
    description = TextAreaField('Description', validators=[
                                Length(min=1, max=200)], description='Description')
    price = FloatField('Price', description='Price')
    is_available = BooleanField('Is Available', description='Is Available')

    def validate_name(self, name):
        if BusinessItem.query.filter_by(name=name.data, user_id=current_user.id).scalar():
            raise ValidationError('Business Item already exists')


class BusinessItemSearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[
                              Length(min=0, max=50)], description='Search Term')


class BusinessItemEditForm(BusinessItemForm):
    def __init__(self, id):
        self.id = id
        super().__init__()

    def validate_name(self, name):
        name = name.data
        business_item = BusinessItem.query.filter_by(
            name=name, user_id=current_user.id).filter(BusinessItem.id != self.id).scalar()
        if business_item:
            raise ValidationError('Business Item already exists')


class BusinessTicketForm(FlaskForm):
    is_business_item = BooleanField(
        'Is Business Item', description='Is Business Item')
    name = StringField('Name', validators=[
                       Length(min=1, max=100)], description='Name')
    business_items = SelectField('Business Items', choices=[])
    requirement = StringField('Requirement (kg/days/nos)', validators=[
        Length(min=1, max=50)], description='Requirement (kg/days/nos)')
