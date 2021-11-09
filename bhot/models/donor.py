from datetime import datetime
from bhot.models import db

class Donor(db.Model):
    __tablename__ = 'donors'

    donor_id = db.Column(db.Integer, primary_key=True)

    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'))

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    external_donor_id = db.Column(db.String,nullable=False)

    # Add fields related to Donor
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
        #db.Enum('male','female', name="donor_gender")) # tehnically this should be "sex"...
    ethnicity = db.Column(db.String)
    dtype = db.Column(db.String)
        #db.Enum('living','DBD','DCD', name="donor_type"))
    cause_of_death = db.Column(db.String)

    # Kidney Donor Risk Index
    kdri = db.Column(db.Integer)

    cold_ischemia = db.Column(db.String)
    diabetes = db.Column(db.String)
    history_of_hypertension = db.Column(db.String)
    other_comorbidity = db.Column(db.String)

    serum_creatinine = db.Column(db.Float)

    proteinuria_dipstick = db.Column(db.String)
        #db.Enum('Absent','Trace','+','++','+++','++++', name="donor_prot_dipstick"))
    proteinuria_date = db.Column(db.DateTime())

    egfr = db.Column(db.Integer)
    egfr_date = db.Column(db.DateTime())

    procurement_date = db.Column(db.DateTime())

    abo_incompatible = db.Column(db.String)
    hla_a_mismatches = db.Column(db.Integer)
    hla_b_mismatches = db.Column(db.Integer)
    hla_dr_mismatches = db.Column(db.Integer)

    #hbv_hbs_ag = db.Column(db.String)
    #hbv_hbs_as = db.Column(db.String)
    #hbv_hbs_ac = db.Column(db.String)

    #proteinuria = db.Column(db.Float

    cold_ischemia_time = db.Column(db.Integer)
    cold_ischemia_units = db.Column(db.String)

    delayed_graft_function = db.Column(db.String)
    # total_hla_mismatches = db.Column(db.Integer)

    induction_therapy = db.Column(db.String)

    preformed_dsa = db.Column(db.String)
    class_immunodominant_dsa = db.Column(db.String)
        #db.Enum('I','II', name="donor_immuno_dsa"))
    specificity_immunodominant_dsa = db.Column(db.String)
    immunodominant_dsa = db.Column(db.String)

    c1qi_binding = db.Column(db.String)

    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="donor")
