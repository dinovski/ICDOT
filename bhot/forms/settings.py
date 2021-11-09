from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms.fields.html5 import DateField

class SettingsForm(FlaskForm):
    option1 = IntegerField('Option 1', validators=[])
    option2 = SelectField('Option 2', validators=[], choices=[("A","A"),("B","B")])
