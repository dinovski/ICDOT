from datetime import datetime
from bhot.models import db

class Molecular(db.Model):
    __tablename__ = 'moleculars'

    molecular_id = db.Column(db.Integer, primary_key=True)
    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    external_biopsy_id = db.Column(db.String,nullable=False)
    run_date = db.Column(db.DateTime())

    rna_concentration = db.Column(db.Float)
    rna_integrity_number = db.Column(db.Integer)

    run_protocol = db.Column(db.String)
    imaging_qc = db.Column(db.Integer)
    binding_density_qc = db.Column(db.Float)
    pos_ctrl_linear = db.Column(db.Float)
    pos_ctrl_limit = db.Column(db.Float)

    rcc_file_name = db.Column(db.String)
    rcc_data = db.Column(db.LargeBinary)

    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="molecular")
