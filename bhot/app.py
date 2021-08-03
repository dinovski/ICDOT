import os,sys
from flask import Flask, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix


from .config import flask_config
from . import app,csrf
from .models import db
from .models.user import User
from .models.demodata import CreateDemoData
from .views import main
from .jobs import rq
from .gunicorn_logging_hack import gunicorn_logging_hack

app.config.update(flask_config)

app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize Cross-Site-Request-Forge protection
csrf.init_app(app)

if app.debug:
    toolbar = DebugToolbarExtension(app)

db.app = app
db.init_app(app)
db.create_all()
db.session.commit()
CreateDemoData()

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


rq.init_app(app)
app.rq = rq

@app.before_first_request
def setup_logging():
    if not app.debug:
        gunicorn_logging_hack(app)

