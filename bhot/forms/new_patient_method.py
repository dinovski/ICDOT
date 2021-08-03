from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, \
    PasswordField, RadioField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms.fields.html5 import DateField

class NewPatientMethodForm(FlaskForm):
    organ = SelectField(
        'Choose organ',
        choices=[('','Choose organ...'),
                 ('kidney', 'kidney'),
                 ('heart', 'heart'),
                 ('liver', 'liver'),
                 ('lung', 'lung')],
        validators=[DataRequired()]
    )

    data_entry_method = RadioField('Data Entry Method',
                                   choices=[('manual','manual'),
                                            ('import','import')],
                                   validators=[DataRequired()])

    def validate_organ(self, field):
        if len(field.data)==0:
            raise ValidationError("Please select an organ")
