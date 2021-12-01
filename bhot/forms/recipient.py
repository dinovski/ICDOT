from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField,ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Optional, NumberRange
from wtforms.fields.html5 import DateField

from bhot.models.recipient import Recipient
from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper

class RecipientForm(FlaskForm):
    external_recipient_id = StringField('Internal Recipient ID', validators=[DataRequired()])

    gender = SelectField(
        'Gender',
        choices=[('', 'N/A'),('female', 'female'), ('male', 'male')]
    )

    date_of_birth = DateField('Date of Birth',
                              validators=[DataRequired()]
    )

    ethnicity = StringField('Ethnicity', validators=[Optional()] )

    nephropathy = StringField('Nephropathy', validators=[Optional()] )

    hiv_status = BooleanSelectFieldHelper('HIV status','positive','negative')

    hbv_hbs_ag = BooleanSelectFieldHelper('HBV HBsAg status','positive','negative')
    hbv_hbs_as = BooleanSelectFieldHelper('HBV HBsAs status','positive','negative')
    hbv_hbs_ac = BooleanSelectFieldHelper('HBV HBsAc status','positive','negative')

    hcv = BooleanSelectFieldHelper('HCV status','positive','negative')

    record_date = DateField('Record Date', validators=[DataRequired()] )

    blood_pressure = IntegerField('Blood Pressure (mm Hg)', validators=[Optional()])

    weight = IntegerField('Weight (kg)', validators=[Optional()])

    disease = StringField("Primary kidney disease",validators=[Optional()])

    egfr = IntegerField('eGFR (mL/min/1.73m2)',
                        validators=[Optional(),NumberRange(min=0,max=120)])
    egfr_date = DateField('eGFR Analysis date', validators=[Optional()] )

    #serum_creatinine = IntegerField('Serum creatinine (mg/dl)', validators=[Optional()])

    proteinuria = IntegerField('Proteinuria',
                               validators=[Optional()])
    proteinuria_units = SelectField('Proteinuria Units',
                                    choices=[
                                        ("g/g","g/g"),
                                        ("g/24h","g/24h"),
                                        ("g/L","g/L"),
                                        ("mg/mmol","mg/mmol"),
                                        ("g/mmol","g/mmol")])

    proteinuria_dipstick = SelectField('Proteinuria (dipstick)',
                                       choices=[('','N/A'),
                                                ('Absent','Absent'),
                                                ('Trace','Trace'),
                                                ('+','+'),
                                                ('++','++'),
                                                ('+++','+++'),
                                               ('++++','++++')])

    proteinuria_date = DateField('Proteinuria date', validators=[Optional()] )

    #treatment = StringField('Treatment')
    #treatment_start_date = DateField('Treatment Start Date', validators=[Optional()] )
    #treatment_end_date = DateField('Treatment End Date', validators=[Optional()] )


    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
