from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', [InputRequired()])
