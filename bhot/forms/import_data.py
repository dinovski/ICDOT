from flask_wtf import FlaskForm
from wtforms import FileField, ValidationError
from wtforms.validators import DataRequired, Optional

class ImportDataForm(FlaskForm):
    xls = FileField('XLS File', validators=[DataRequired()])
    rcc = FileField('RCC File', validators=[Optional()])
