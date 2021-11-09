from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from bhot import app,csrf
from bhot.models import db
from bhot.models.group import Group
from bhot.models.transplant import Transplant
from bhot.forms.transplant import TransplantForm

from pprint import pprint

@app.route("/transplant/add", methods=["GET","POST"])
@login_required
def transplant_add():
    f = TransplantForm()
    if f.validate_on_submit():
        # If the user requres data import, redirect there.
        if f.data_entry_method.data == "import":
            return redirect(url_for("import_data"))

        # Otherwise, create a new transplant record
        t = Transplant()
        f.copy_to_db_model(t)
        t.created_by_user_id = current_user.user_id
        t.group_id = current_user.group_id
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("transplant_show", tid=t.transplant_id))
    return render_template("new-transplant.html", form=f,
                           submit_button_label="Add Transplant")



@app.route("/transplant/show/<tid>")
@login_required
def transplant_show(tid):
    t = Transplant.query.filter_by(transplant_id=tid).first_or_404()

    return render_template("transplant-view.html", transplant=t)
