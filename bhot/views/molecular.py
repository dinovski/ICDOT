from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.molecular import Molecular
from bhot.forms.molecular import MolecularForm

@app.route("/molecular/add/<tid>", methods=["GET","POST"])
@login_required
def molecular_add(tid):
    t = Transplant.query.get_or_404(tid)
    pprint(t)
    if t.molecular:
        abort(400)

    f = MolecularForm()
    if f.validate_on_submit():
        m = Molecular()
        m.created_by_user_id = current_user.user_id
        t.molecular = m
        f.copy_to_db_model(m)
        db.session.add(t)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=tid))
    else:
        pprint(f.errors)

    return render_template("new-molecular.html", form=f,tid=tid,
                           submit_button_label="Add Molecular")


@app.route("/molecular/edit/<id>", methods=["GET","POST"])
@login_required
def molecular_edit(id):
    m = Molecular.query.get_or_404(id)

    f = MolecularForm()

    if f.validate_on_submit():
        f.copy_to_db_model(m)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for("grafts_edit", tid=m.transplant.transplant_id))
    else:
        pprint(f.errors)
        f.copy_from_db_model(m)

    return render_template("new-molecular.html", form=f,tid=m.transplant.transplant_id,
                           submit_button_label="Update Molecular")
