from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DecimalField, ValidationError, FileField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Required
from wtforms.fields.html5 import DateField

from bhot.models.molecular import Molecular

from .utils import copy_db_model_to_wtform, copy_wtform_to_db_model, BooleanSelectFieldHelper


class MolecularForm(FlaskForm):

    external_biopsy_id = StringField('Biopsy ID',validators=[DataRequired()])

    run_date = DateField('Run date', validators=[DataRequired()] )

    rna_concentration = DecimalField("RNA concentration (ng/ul)",
                                     validators=[Optional(), NumberRange(min=0,max=1000)])

    rna_integrity_number = DecimalField("RNA integrity number (RIN)",
                                     validators=[Optional(), NumberRange(min=0,max=10)])

    run_protocol =  SelectField(
        'Run protocol',
        choices=[('','N/A'),
                 ('high_sensitivity', 'High sensitivity (default)'),
                 ('standard','Standard')]    )

    imaging_qc = IntegerField("Imaging QC",
                               validators=[Optional(), NumberRange(min=0,max=500)])

    binding_density_qc = DecimalField("Binding Density QC",
                                     validators=[Optional(), NumberRange(min=0,max=500)])

    pos_ctrl_linear = DecimalField("Positive Control Linearity QC",
                                     validators=[Optional(), NumberRange(min=0,max=500)])
    pos_ctrl_limit = DecimalField("Positive Control Limit of Detection QC",
                                     validators=[Optional(), NumberRange(min=0,max=500)])

    rcc_data = FileField('RCC File')


    def copy_to_db_model(self,r):
        copy_wtform_to_db_model(self,r)

    def copy_from_db_model(self,r):
        copy_db_model_to_wtform(self,r)
