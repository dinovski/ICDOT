from datetime import datetime
from bhot.models import db

class Recipient(db.Model):
    __tablename__ = 'recipients'

    recipient_id = db.Column(db.Integer, primary_key=True)

    transplant_id = db.Column(db.Integer, db.ForeignKey('transplants.transplant_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)


    date_of_birth = db.Column(db.DateTime())

    # add any fields related to a patient
    external_recipient_id = db.Column(db.String,nullable=False)
    gender = db.Column(db.String)
        #db.Enum('male','female',name="recipient_gender"), nullable=True)

    ethnicity = db.Column(db.String)
    nephropathy = db.Column(db.String)

    hiv = db.Column(db.String)
    hbv_hbs_ag = db.Column(db.String)
    hbv_hbs_as = db.Column(db.String)
    hbv_hbs_ac = db.Column(db.String)
    hcv = db.Column(db.String)

    record_date = db.Column(db.DateTime())
    blood_pressure = db.Column(db.String)
    weight = db.Column(db.Float)
    disease = db.Column(db.String)

    egfr = db.Column(db.Integer)
    egft_date = db.Column(db.DateTime())

    proteinuria = db.Column(db.Float)
    proteinuria_units = db.Column(db.String)
        #db.Enum(
        #"g/g", "g/24h", "g/L", "mg/mmol", "g/mmol",
        #name="recipient_proteinuria_units"))

    proteinuria_dipstick = db.Column(db.String)
        #db.Enum('Absent','Trace','+','++','+++','++++', name="recipient_prot_dipstick"))
    proteinuria_date = db.Column(db.DateTime())


    # Relationships
    transplant = db.relationship("Transplant", uselist=False, back_populates="recipient")
