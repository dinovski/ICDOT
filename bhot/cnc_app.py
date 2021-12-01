import os,sys
from redis import Redis
from pprint import pprint

from flask import Flask
from flask_login import current_user
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib import rediscli
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail

import rq_dashboard

from .config import flask_config
from . import app,csrf
from .models import db
from .models.user import User
from .models.recipient import Recipient
from .models.donor import Donor
from .models.followup import FollowUp
from .cnc_views import cnc_main
from .cnc_views import user_management
from .jobs import rq

app.config.update(flask_config)

if app.debug:
    toolbar = DebugToolbarExtension(app)

db.app = app
db.init_app(app)

rq.init_app(app)
app.rq = rq

mail = Mail(app)

admin = Admin(app, name='ICDOT', template_mode='bootstrap3')

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

admin.add_view(ModelView(User, db.session, category="Database"))
admin.add_view(ModelView(Recipient, db.session, category="Database"))
admin.add_view(ModelView(Donor,     db.session, category="Database"))
admin.add_view(ModelView(FollowUp,  db.session, category="Database"))

#admin.add_sub_category(name="Links", parent_name="Database")
admin.add_link(MenuLink(name='RQ-worker', url='/rq', category="Rmarkdown Jobs"))
admin.add_view(rediscli.RedisCli(Redis(), category="Rmarkdown Jobs"))

