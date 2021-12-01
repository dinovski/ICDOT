from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, ValidationError, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField

from bhot.models.donor import Donor

from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper



class DonorForm(FlaskForm):

    external_donor_id = StringField('Internal Donor ID',validators=[DataRequired()])

    age = IntegerField('age', validators=[Optional()])

    gender = SelectField(
        'Gender',
        choices=[('', 'N/A'),('female', 'female'), ('male', 'male')]
    )

    ethnicity = StringField('Ethnicity',validators=[Optional()])

    dtype = SelectField(
        'Donor Type',
        choices=[('', 'N/A'),
                 ('living', 'living'),
                 ('DBD', 'Donation after Brain Death'),
                 ('DCD','Donation after Circulatory Death')]
    )
    cause_of_death = StringField('Cause of Death')

    kdri = IntegerField('Kidney Donor Risk Index (%)',validators=[Optional()])

    diabetes = BooleanSelectFieldHelper('Diabetes','yes','no')

    history_of_hypertension = BooleanSelectFieldHelper('History of Hypertension','yes','no')

    other_comorbidities = StringField('Other Comorbidities',validators=[Optional()])

    serum_creatinine = DecimalField("Serum creatinine (mg/dl)",validators=[Optional()])

    proteinuria_dipstick = SelectField('Proteinuria (dipstick)',
                                       choices=[('','N/A'),
                                                ('Absent','Absent'),
                                                ('Trace','Trace'),
                                                ('+','+'),
                                                ('++','++'),
                                                ('+++','+++'),
                                                ('++++','++++')])

    proteinuria_date = DateField('Proteinuria date',validators=[Optional()])

    egfr = IntegerField('eGFR (mL/min/1.73m2)',
                        validators=[Optional(),NumberRange(min=0,max=120)])
    egfr_date = DateField('eGFR analysis date',validators=[Optional()])

    procurement_date = DateField('Procurement date',validators=[Optional()])


    #proteinuria = IntegerField('Proteinuria (g/g or g/24h)',
    #                           validators=[Optional()])

    abo_incompatible = BooleanSelectFieldHelper('ABO incompatible','yes','no')

    hla_a_mismatches = IntegerField('Total HLA-A mismatches',
                                      validators=[Optional(), NumberRange(min=0,max=6)])
    hla_b_mismatches = IntegerField('Total HLA-B mismatches',
                                      validators=[Optional(), NumberRange(min=0,max=6)])
    hla_dr_mismatches = IntegerField('Total HLA-DR mismatches',
                                      validators=[Optional(), NumberRange(min=0,max=6)])

    cold_ischemia_time = IntegerField('Cold ischemia time',
                                      validators=[Optional()])
    cold_ischemia_units = SelectField('Cold ischemia units',
                                       choices=[('minutes','minutes'),
                                                ('hours','hours')])


    delayed_graft_function = BooleanSelectFieldHelper('Delayed graft function','yes','no')

    #total_hla_mismatches =  IntegerField('Total HLA mismatches',
    #                                     validators=[Optional()])

    induction_therapy = StringField('Induction Therapy')

    preformed_dsa = BooleanSelectFieldHelper('Preformed DSA','positive','negative')

    class_immunodominant_dsa = SelectField('Class (immunodom. DSA)',
                                       choices=[('','N/A'),
                                                ('I','I (A, B, Cw)'),
                                                ('II','II (DR, DQ, DP)')])

    specificity_immunodominant_dsa = StringField('Specificity (immunodominant DSA)')

    immunodominant_dsa = StringField('Immunodominant DSA (MFI)')

    c1qi_binding = BooleanSelectFieldHelper('C1q binding','yes','no')


    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
