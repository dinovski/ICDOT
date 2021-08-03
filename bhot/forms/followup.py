from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField

from bhot.models.followup import FollowUp

from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model

class FollowUpForm(FlaskForm):

    record_date = DateField('Record Date', validators=[DataRequired()] )

    blood_pressure = IntegerField('Blood Pressure (mm Hg)', validators=[Optional()])

    weight = IntegerField('Weight (Kg)', validators=[Optional()])

    egfr = IntegerField('eGFR (mL/min/1.73m2)',
                        validators=[Optional(),NumberRange(min=0,max=120)])

    serum_creatinine = IntegerField('Serum creatinine', validators=[Optional()])
    serum_creatinine_units = SelectField("Units", choices=[("mg/dL","mg/dL"),("µmol/L","µmol/L")])

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

    graft_loss_date = DateField('Graft Loss', validators=[Optional()] )
    death_date = DateField('Patient Death', validators=[Optional()] )


    immunosuppressive_drug = SelectField('Immunosuppressive drug',
                                         choices=[('','N/A'),
                                                  ("Tacrolimus/Ciclosporine","Tacrolimus/Ciclosporine"),
                                                   ("MPA","MPA"),
                                                   ("MMF","MMF"),
                                                   ("Everolimus/Sirolimus","Everolimus/Sirolimus"),
                                                   ("Azathioprine","Azathioprine"),
                                                   ("Belatacept","Belatacept"),
                                                   ("Steroids","Steroids")])

    immunosuppressive_drug_daily_dosage = DecimalField('Daily Dosage (mg)', validators=[Optional()])


    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
