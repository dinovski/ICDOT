from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bhot.models import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'),nullable=False)

    # Records keeping
    created = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

    email = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(1024))
    active = db.Column(db.Boolean,nullable=False,default=True)
    registered_at = db.Column(db.DateTime(),default=datetime.utcnow)
    validated = db.Column(db.Boolean,nullable=False,default=False)
    validated_at = db.Column(db.DateTime())

    first_name = db.Column(db.String(255))
    last_name  = db.Column(db.String(255))
    institute  = db.Column(db.String(255))
    department = db.Column(db.String(255))

    @property
    def id(self):
        return self.user_id

    def get_id(self):
        return self.user_id

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256:10000')
        return True

    def check_password(self, password):
        return check_password_hash(self.password, password)
