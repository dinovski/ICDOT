from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.followup import FollowUp
from bhot.forms.followup import FollowUpForm

@app.route("/followup/add/<tid>", methods=["GET","POST"])
@login_required
def followup_add(tid):
    t = Transplant.query.get_or_404(tid)

    f = FollowUpForm()
    if f.validate_on_submit():
        fu = FollowUp()
        f.copy_to_db_model(fu)
        fu.created_by_user_id = current_user.user_id
        t.followups.append(fu)
        db.session.add(fu)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=tid)+"#nav-followups")

    return render_template("new-followup.html", form=f,tid=tid,
                           submit_button_label="Add Follow-up")


@app.route("/followup/edit/<id>", methods=["GET","POST"])
@login_required
def followup_edit(id):
    fu = FollowUp.query.get_or_404(id)

    ff = FollowUpForm()

    if ff.validate_on_submit():
        ff.copy_to_db_model(fu)
        db.session.add(fu)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=fu.transplant.transplant_id)+"#nav-followups")
    else:
        ff.copy_from_db_model(fu)

    return render_template("new-followup.html", form=ff,tid=fu.transplant.transplant_id,
                           submit_button_label="Update Follow-up")
