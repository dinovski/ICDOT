from datetime import datetime
from bhot.models import db

class ClinicalBiopsy(db.Model):
    __tablename__ = 'clinical_biopsies'

    clinical_biopsy_id = db.Column(db.Integer, primary_key=True)
    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    external_biopsy_id = db.Column(db.String)

    #external_donor_id = db.Column(db.String)
    #transplant_date = db.Column(db.DateTime())

    biopsy_date = db.Column(db.DateTime())

    pretransplant_biopsy = db.Column(db.String)
    biopsy_indication = db.Column(db.String)

    serum_creatinine = db.Column(db.Float)
    serum_creatinine_units = db.Column(db.String)

    proteinuria = db.Column(db.Float)
    proteinuria_units = db.Column(db.String)
        #db.Enum(
        #"g/g", "g/24h", "g/L", "mg/mmol", "g/mmol",
        #name="recipient_proteinuria_units"))

    proteinuria_dipstick = db.Column(db.String)
        #db.Enum('Absent','Trace','+','++','+++','++++', name="recipient_prot_dipstick"))
    proteinuria_date = db.Column(db.DateTime())

    current_immunosuppressant = db.Column(db.String)
    current_treatment_dose = db.Column(db.Float)

    rejection_treatment = db.Column(db.String)
    treatment_start_date = db.Column(db.DateTime())

    polyoma_virus_pcr = db.Column(db.Integer)

    cell_free_dna_level = db.Column(db.Integer)

    bkv_load = db.Column(db.Integer)
    bkv_load_units = db.Column(db.String)

    #immunosuppressive_therapy = db.Column(db.String)


    preformed_dsa = db.Column(db.String)

    dsa_history = db.Column(db.String)

    dsa_class = db.Column(db.String)

    # iDSA = immunodominant DSA
    idsa_class = db.Column(db.String)

    idsa_specificity = db.Column(db.String)

    idsa_mfi = db.Column(db.String)

    c1qi_binding = db.Column(db.String)

    non_anti_hla_dsa = db.Column(db.String)

    non_anti_hla_dsa_type = db.Column(db.String)

    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="clinical_biopsy")

"""
biopsy_date
polyoma_virus_pcr
cell_free_dna_level
immunosuppressive_therapy
preformed_dsa
history
class_immunodominant_dsa
specificity_immunodominant_dsa
c1q_binding
mfi_immunodominant_dsa
non_anti_hla_dsa
non_anti_hla_dsa_type
pre_transplant_biopsy
biopsy_indication
treatment
treatment_start_date
treatment_end_date
"""
