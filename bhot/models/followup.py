from datetime import datetime
from bhot.models import db

class FollowUp(db.Model):
    __tablename__ = 'followups'

    followup_id = db.Column(db.Integer, primary_key=True)
    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    #external_recipient_id = db.Column(db.String)

    record_date = db.Column(db.DateTime())

    blood_pressure = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    egfr = db.Column(db.Integer)

    serum_creatinine = db.Column(db.Float)
    serum_creatinine_units = db.Column(db.String)

    proteinuria = db.Column(db.Float)
    proteinuria_units = db.Column(db.String)
        #db.Enum(
        #"g/g", "g/24h", "g/L", "mg/mmol", "g/mmol",
        #name="recipient_proteinuria_units"))

    proteinuria_dipstick = db.Column(db.String)
        #db.Enum('Absent','Trace','+','++','+++','++++', name="recipient_prot_dipstick"))

    graft_loss_date = db.Column(db.DateTime())

    death_date = db.Column(db.DateTime())

    immunosuppressive_drug = db.Column(db.String)

    immunosuppressive_drug_daily_dosage = db.Column(db.String)

    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="followups")
