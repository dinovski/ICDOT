from datetime import datetime
from bhot.models import db

class Transplant(db.Model):
    __tablename__ = 'transplants'

    transplant_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'),nullable=False)

    # Records keeping
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),nullable=False)
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    transplant_date = db.Column(db.DateTime(),nullable=False)
    organ = db.Column(db.String,nullable=False)



    # Relationships
    group = db.relationship("Group", uselist=False, back_populates="transplants")

    recipient = db.relationship("Recipient", uselist=False, back_populates="transplant")
    donor = db.relationship("Donor", uselist=False, back_populates="transplant")
    clinical_biopsy = db.relationship("ClinicalBiopsy", uselist=False, back_populates="transplant")
    histology = db.relationship("Histology", uselist=False, back_populates="transplant")
    molecular = db.relationship("Molecular", uselist=False, back_populates="transplant")

    followups = db.relationship("FollowUp", back_populates="transplant")


    @property
    def completed(self):
        return (self.donor != None
                and self.recipient != None
                and self.clinical_biopsy != None
                and self.histology != None
                and self.molecular != None)


    @property
    def status(self):
        if self.completed:
            return "COMPLETED"
        else:
            return "INCOMPLETE"
