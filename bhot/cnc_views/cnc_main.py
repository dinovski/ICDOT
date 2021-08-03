from datetime import datetime
from time import sleep
import os, json, random
from os.path import dirname
from subprocess import Popen,PIPE
from flask import render_template, request, flash, redirect, url_for, send_file
from flask_mail import Message
from tempfile import NamedTemporaryFile
from werkzeug.utils import secure_filename
from pprint import pprint

from bhot import app


@app.route("/")
def index():
    return render_template("cnc-index.html")


@app.route("/test-send-email",methods=["POST"])
def test_send_email():
    rcpt = request.form.get('email')
    if not rcpt:
        flash("Missing Email Address","danger")
        return redirect(url_for("index"))

    msg = Message("ICDOT TEST EMAIL",
                  recipients=[rcpt])
    msg.body = "This is a test message from ICDOT-CNC"
    mail = app.extensions['mail']
    mail.send(msg)

    flash("Email to '%s' Queued" % (rcpt),"info")
    return redirect(url_for("index"))
