from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.donor import Donor
from bhot.forms.donor import DonorForm

@app.route("/donor/add/<tid>", methods=["GET","POST"])
@login_required
def donor_add(tid):
    t = Transplant.query.get_or_404(tid)
    pprint(t)
    if t.donor:
        abort(400)

    f = DonorForm()
    if f.validate_on_submit():
        d = Donor()
        d.created_by_user_id = current_user.user_id
        t.donor = d
        f.copy_to_db_model(d)
        db.session.add(t)
        db.session.add(d)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=tid)+"#nav-donor")

    return render_template("new-donor.html", form=f,tid=tid,
                           submit_button_label="Add Donor")


@app.route("/donor/edit/<id>", methods=["GET","POST"])
@login_required
def donor_edit(id):
    d = Donor.query.get_or_404(id)
    f = DonorForm()

    if f.validate_on_submit():
        f.copy_to_db_model(d)
        db.session.add(d)
        db.session.commit()
        # using url_for(...,_anchor="nav-donor") doesn't work, see
        # https://stackoverflow.com/q/21583594
        return redirect(url_for("transplant_show", tid=d.transplant.transplant_id) + "#nav-donor")
    else:
        f.copy_from_db_model(d)

    return render_template("new-donor.html", form=f,tid=d.transplant.transplant_id,
                           submit_button_label="Update Donor")
