from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.histology import Histology
from bhot.forms.histology import HistologyForm

@app.route("/histology/add/<tid>", methods=["GET","POST"])
@login_required
def histology_add(tid):
    t = Transplant.query.get_or_404(tid)
    pprint(t)
    if t.histology:
        abort(400)

    f = HistologyForm()
    if f.validate_on_submit():
        h = Histology()
        h.created_by_user_id = current_user.user_id
        t.histology = h
        f.copy_to_db_model(h)
        db.session.add(t)
        db.session.add(h)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=tid))
    else:
        pprint(f.errors)

    return render_template("new-histology.html", form=f,tid=tid,
                           submit_button_label="Add Histology")

@app.route("/histology/edit/<id>", methods=["GET","POST"])
@login_required
def histology_edit(id):
    h = Histology.query.get_or_404(id)

    f = HistologyForm()

    if f.validate_on_submit():
        f.copy_to_db_model(h)
        db.session.add(h)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=h.transplant.transplant_id))
    else:
        pprint(f.errors)
        f.copy_from_db_model(h)

    return render_template("new-histology.html", form=f,tid=h.transplant.transplant_id,
                           submit_button_label="Update Histology")
