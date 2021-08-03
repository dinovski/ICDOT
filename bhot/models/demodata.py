from datetime import datetime
from werkzeug.security import generate_password_hash

from . import db
from .group import Group
from .user import User

def CreateGroupData():
    if Group.query.filter_by(institute="DEMO").count() != 0:
        return

    g = Group()
    g.institute = "DEMO"
    g.department = "DEMO"
    db.session.add(g)
    db.session.commit()

def CreateUserData():
    grp = Group.query.filter_by(institute="DEMO").first()

    data = [
        {
            "email" : "icdot2@housegordon.com",
            "password" :  generate_password_hash("12345", method='pbkdf2:sha256:10000'),
            "first_name" : "Assaf",
            "last_name" : "Gordon",
            "institute" : "foo",
            "department": "bar",
        },
        {
            "email" : "dina.zielinski@paristransplantgroup.org",
            "password" : "pbkdf2:sha256:10000$tbJ7L5p3$31a9ae7308d6938abe4da33c7f92ce7f08f3112b767357183cf5c79702ad22be",
            "first_name" : "Dina",
            "last_name" : "Z",
            "institute" : "PTG",
            "department": "kidney",
        }

        ]

    for d in data:
        if User.query.filter_by(email=d["email"]).first():
            continue

        u = User()
        u.group_id = grp.group_id
        u.email = d["email"]
        u.password = d["password"]
        u.first_name = d["first_name"]
        u.last_name = d["last_name"]
        u.institute = d["institute"]
        u.department = d["department"]
        u.validated = True
        u.validated_at = datetime.utcnow()
        u.active = True

        db.session.add(u)
        db.session.commit()


def CreateDemoData():
    CreateGroupData()
    CreateUserData()
