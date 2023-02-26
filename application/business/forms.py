from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import Length, ValidationError

from application.business.models import BusinessSubType, BusinessType


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
