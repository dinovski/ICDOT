from pprint import pprint

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.transplant import Transplant
from bhot.models.recipient import Recipient
from bhot.forms.recipient import RecipientForm

@app.route("/recipient/add/<tid>", methods=["GET","POST"])
@login_required
def recipient_add(tid):
    t = Transplant.query.get_or_404(tid)
    pprint(t)
    if t.recipient:
        abort(400)

    f = RecipientForm()
    if f.validate_on_submit():
        r = Recipient()
        r.created_by_user_id = current_user.user_id
        t.recipient = r
        f.copy_to_db_model(r)
        db.session.add(t)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=tid))

    return render_template("new-recipient.html", form=f,tid=tid,
                           submit_button_label="Add Recipient")


@app.route("/recipient/edit/<id>", methods=["GET","POST"])
@login_required
def recipient_edit(id):
    r = Recipient.query.get_or_404(id)

    f = RecipientForm()
    if f.validate_on_submit():
        f.copy_to_db_model(r)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=r.transplant.transplant_id))
    else:
        f.copy_from_db_model(r)

    return render_template("new-recipient.html", form=f,tid=r.transplant.transplant_id,
                           submit_button_label="Update Recipient")
