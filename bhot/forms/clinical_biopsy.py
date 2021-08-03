from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField

from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper

from bhot.models.clinical_biopsy import ClinicalBiopsy


class ClinicalBiopsyForm(FlaskForm):

    external_biopsy_id = StringField('Internal Biopsy ID',validators=[DataRequired()])
    #external_donor_id = StringField('Internal Donor ID',validators=[DataRequired()])

    #transplant_date = DateField('Transplante Date', validators=[DataRequired()] )
    biopsy_date = DateField('Biopsy Date', validators=[DataRequired()] )

    pretransplant_biopsy = SelectField('Pre-transplant biopsy',
                                       choices=[('','N/A'),
                                                ('procurement','procurement'),
                                                ('preimplantation','preimplantation')])

    biopsy_indication = StringField('Biopsy indication')


    serum_creatinine = IntegerField('Serum creatinine (mg/dl)', validators=[Optional()])
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


    proteinuria_date = DateField('Proteinuria date', validators=[Optional()] )

    current_immunosuppressant = SelectField('Current Immunosuppressant',
                                         choices=[('NA','N/A'),
                                                  ("Tacrolimus/Ciclosporine","Tacrolimus/Ciclosporine"),                                                   ("MPA","MPA"),
                                                   ("MMF","MMF"),
                                                   ("Everolimus/Sirolimus","Everolimus/Sirolimus"),
                                                   ("Azathioprine","Azathioprine"),
                                                   ("Belatacept","Belatacept"),
                                                   ("Steroids","Steroids")])
    current_treatment_dose = DecimalField('Dose',validators=[Optional()])

    rejection_treatment = SelectField('Rejection Treatment',
                                      choices=[
                                          ("NA","NA"),
                                          ("IV corticosteroids","IV corticosteroids"),
                                          ("IVIG","IVIG"),
                                          ("Plasmapharesis","Plasmapharesis"),
                                          ("Rituximab","Rituximab"),
                                          ("ATG (Thymoglobulin)","ATG (Thymoglobulin)"),
                                          ("Eculizimab","Eculizimab"),
                                          ("Alemtuzumab","Alemtuzumab"),
                                          ("Bortezomib","Bortezomib")
                                          ])

    treatment_start_date = DateField('Treatment Start Date', validators=[Optional()] )

    polyoma_virus_pcr = IntegerField('Polyoma virus PCR (log)', validators=[Optional()])

    cell_free_dna_level = IntegerField('cell-free DNA level', validators=[Optional()])

    bkv_load = IntegerField('BKV Load', validators=[Optional()])
    bkv_load_units = SelectField("BKL Units", choices=[
        ("copies/mL","copies/mL"),
        ("log/mL","log/mL")
        ])

    preformed_dsa = BooleanSelectFieldHelper('Preformed DSA','positive','negative')

    dsa_history = SelectField(
        'DSA History',
        choices=[('', 'N/A'),
                 ('denovo', 'de novo'),
                 ('persistent', 'persistent')]
    )
    dsa_class = SelectField('DSA Class',
                                       choices=[('','N/A'),
                                                ('I','I'),
                                                ('II','II'),
                                                ('I/II','I/II')])


    idsa_class = SelectField('immunodom. DSA Class',
                                       choices=[('','N/A'),
                                                ('I','I (A, B, Cw)'),
                                                ('II','II (DR, DQ, DP)')])

    idsa_specificity = StringField('immunodominant DSA class specificity')

    idsa_mfi = StringField("Immunodominant DSA MFI")

    c1qi_binding = BooleanSelectFieldHelper('C1q binding','positive','negative')

    non_anti_hla_dsa = BooleanSelectFieldHelper('Non anti-HLA DSA','positive','negative')

    non_anti_hla_dsa_type = StringField('Non anti-HLA DSA type')



    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
