from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, \
    PasswordField, RadioField, ValidationError, Form
from wtforms.validators import DataRequired, EqualTo, Required, Optional
from wtforms.fields.html5 import DateField

from bhot.models.transplant import Transplant
from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper

class TransplantForm(FlaskForm):
    organ = SelectField(
        'Choose organ',
        choices=[('','Choose organ...'),
                 ('kidney', 'kidney'),
                 ('heart', 'heart'),
                 ('liver', 'liver'),
                 ('lung', 'lung')],
        validators=[Required()]
    )

    data_entry_method = RadioField('Data Entry Method',
                                   choices=[('manual','manual'),
                                            ('import','import')],
                                   validators=[Required()])

    transplant_date = DateField('Transplant Date',
                                validators=[Optional()])

    def validate_organ(self, field):
        if len(field.data)==0:
            raise ValidationError("Please select an organ")
        if field.data != "kidney":
            raise ValidationError("%s transplants are not supported yet" % field.data)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.data_entry_method.data == "manual" and \
           self.transplant_date.data is None:
            self.transplant_date.errors.append("Missing transplant date")
            return False
        return True

    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
