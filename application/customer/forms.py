from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class BusinessSearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[
                              Length(min=0, max=50)], description='Search Term')
