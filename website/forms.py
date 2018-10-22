from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    choices = [('Heirloom', 'Heirloom'),
               ('Standard', 'Standard'),
               ('Modern', 'Modern'),
               ('Legacy', 'Legacy')]
    select = SelectField('Format:', choices=choices)
    q = StringField('q', validators=[DataRequired()])
