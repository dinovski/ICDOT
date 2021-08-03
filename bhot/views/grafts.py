from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.group import Group
from bhot.models.transplant import Transplant
from bhot.forms.transplant import TransplantForm

from pprint import pprint

@app.route("/grafts/edit/<tid>", methods=["GET","POST"])
@login_required
def grafts_edit(tid):
    t = Transplant.query.get_or_404(tid)
    return render_template("grafts-edit.html", transplant=t)
