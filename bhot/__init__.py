# -*- coding: utf-8 -*-
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Make CSRF object a global variable,
# so that all views could import it and do '@csrf.exempt' with ease.
# The actual flask-app initialization happens in 'mainapp.py'
# after configuration data is loaded.
csrf = CSRFProtect()
