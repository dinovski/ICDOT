from datetime import datetime
from bhot.models import db

class Histology(db.Model):
    __tablename__ = 'histologies'

    histology_id = db.Column(db.Integer, primary_key=True)
    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    external_biopsy_id = db.Column(db.String,nullable=False)

    #external_donor_id = db.Column(db.String,nullable=False)

    biopsy_date =  db.Column(db.DateTime())


    ## Indications

    biopsy_assessment = db.Column(db.String)

    biopsy_method = db.Column(db.String)

    tissue_technique = db.Column(db.String)

    num_glomeruli = db.Column(db.Integer)

    num_glomerulosclerosis = db.Column(db.String)

    num_arteries = db.Column(db.String)

    biopsy_assessment_quality = db.Column(db.String)

    atn = db.Column(db.String)

    tma = db.Column(db.String)
    tma_location = db.Column(db.String)

    acute_lesions_g  = db.Column(db.String)
    acute_lesions_ptc = db.Column(db.String)
    acute_lesions_i = db.Column(db.String)
    acute_lesions_t = db.Column(db.String)
    acute_lesions_v = db.Column(db.String)
    acute_lesions_c4d = db.Column(db.String)
    acute_lesions_c4d_technique = db.Column(db.String)
    ### CHRONIC LESIONS:
    chronic_lesions_cg = db.Column(db.String)
    chronic_lesions_ci = db.Column(db.String)
    chronic_lesions_ct = db.Column(db.String)
    chronic_lesions_cv = db.Column(db.String)
    chronic_lesions_ah = db.Column(db.String)
    chronic_lesions_mm = db.Column(db.String)

    ## ACUTE & CHRONIC LESIONS
    acute_chronic_lesions_ti = db.Column(db.String)
    acute_chronic_lesions_i_ifta = db.Column(db.String)
    acute_chronic_lesions_ifta_pct = db.Column(db.Integer)
    acute_chronic_lesions_t_ifta = db.Column(db.String)
    acute_chronic_lesions_pvl = db.Column(db.String)

    ##  IMMUNOHISTOCHEMISTRY
    immunohistochemistry_sv40_t = db.Column(db.String)
    immunohistochemistry_other = db.Column(db.String)

    ## ELECTRON MICROSCOPY
    electron_microscopy_edd = db.Column(db.String)
    electron_microscopy_edd_location = db.Column(db.String)
    electron_microscopy_tg_cg = db.Column(db.String)
    electron_microscopy_pctml = db.Column(db.String)
    electron_microscopy_other = db.Column(db.String)

    ## IMMUNOFLUORESCENCE
    immunofluorescence_ig_g = db.Column(db.String)
    immunofluorescence_ig_g_location = db.Column(db.String)
    immunofluorescence_ig_a = db.Column(db.String)
    immunofluorescence_ig_a_location = db.Column(db.String)
    immunofluorescence_ig_m = db.Column(db.String)
    immunofluorescence_ig_m_location = db.Column(db.String)
    immunofluorescence_c3   = db.Column(db.String)
    immunofluorescence_c3_location   = db.Column(db.String)
    immunofluorescence_c1q  = db.Column(db.String)
    immunofluorescence_c1q_location  = db.Column(db.String)
    immunofluorescence_kappa = db.Column(db.String)
    immunofluorescence_kappa_location = db.Column(db.String)
    immunofluorescence_lambda = db.Column(db.String)
    immunofluorescence_lambda_location = db.Column(db.String)
    immunofluorescence_other = db.Column(db.String)


    ### Diagnosis
    rejection_diagnosis = db.Column(db.String)
    nonrejection_diagnosis = db.Column(db.String)
    diagnosis_comments = db.Column(db.String)

    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="histology")
