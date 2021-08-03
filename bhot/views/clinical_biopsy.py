from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.clinical_biopsy import ClinicalBiopsy
from bhot.forms.clinical_biopsy import ClinicalBiopsyForm

@app.route("/clinical-biopsy/add/<tid>", methods=["GET","POST"])
@login_required
def clinical_biopsy_add(tid):
    t = Transplant.query.get_or_404(tid)
    pprint(t)
    if t.clinical_biopsy:
        abort(400)

    f = ClinicalBiopsyForm()
    if f.validate_on_submit():
        c = ClinicalBiopsy()
        c.created_by_user_id = current_user.user_id
        t.clinical_biopsy = c
        f.copy_to_db_model(c)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=tid))

    return render_template("new-clinical-biopsy.html", form=f ,tid=tid,
                           submit_button_label="Add Biopsy")

@app.route("/clinical-biopsy/edit/<id>", methods=["GET","POST"])
@login_required
def clinical_biopsy_edit(id):
    c = ClinicalBiopsy.query.get_or_404(id)

    f = ClinicalBiopsyForm()

    if f.validate_on_submit():
        f.copy_to_db_model(c)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=c.transplant.transplant_id))
    else:
        f.copy_from_db_model(c)

    return render_template("new-clinical-biopsy.html", form=f, tid=c.transplant.transplant_id,
                           submit_button_label="Update Biopsy")
