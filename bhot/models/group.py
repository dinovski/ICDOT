from datetime import datetime

from bhot.models import db

class Group(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)

    # Records keeping
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    institute  = db.Column(db.String(255))
    department = db.Column(db.String(255))

    # Relationships
    transplants = db.relationship("Transplant", back_populates="group")
