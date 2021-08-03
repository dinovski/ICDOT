from datetime import datetime
import logging
from flask import render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user, login_required

from sqlalchemy.exc import IntegrityError

from bhot import app
from bhot.models import db
from bhot.models.user import User
from bhot.models.group import Group
from bhot.forms.login import LoginForm
from bhot.forms.register import RegisterForm
from bhot.forms.settings import SettingsForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    next = request.args.get('next')
    # is_safe_url should check if the url is safe for redirects.
    # See http://flask.pocoo.org/snippets/62/ for an example.
    #if not is_safe_url(next):
    #    return flask.abort(400)

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        pw = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(pw):
            login_user(user)
            return redirect(next or flask.url_for('index'))

        flash("Incorrect email or password","danger")

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()


        u = User()
        u.email = email
        u.first_name = form.first_name.data.strip()
        u.last_name = form.last_name.data.strip()
        u.institute = form.institute_name.data.strip()
        u.department = form.department.data.strip()
        u.set_password(form.password.data)

        # During Demo stage, all users are automatically validated
        g = Group.query.filter_by(institute="DEMO").first_or_404()
        u.group_id = g.group_id
        u.validated = True
        u.validated_at = datetime.utcnow()
        u.active = True

        db.session.add(u)
        try:
            db.session.commit()
            flash("user '%s' created. Please Login" % email,"info")
            return redirect(url_for("index"))

        except IntegrityError as e:
            logging.error("register error: %s" % (str(e)))
            flash("Failed to add user '%s': already exists" % email,"danger")

    return render_template("register.html", form=form)



@app.route("/settings",methods=['GET','POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("settings.html", form=form)
