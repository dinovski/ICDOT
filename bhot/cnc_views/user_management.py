from datetime import datetime
import os, json, random
from pprint import pprint

from flask import render_template, request, flash, redirect, url_for, send_file
from flask_mail import Message
from sqlalchemy.exc import IntegrityError

from bhot import app
from bhot.models import db
from bhot.models.user import User

@app.route("/users")
def users():
    users = User.query.order_by(User.user_id).all()
    return render_template("cnc-user-management.html", users=users)


@app.route("/users/create-new-user",methods=["POST"])
def create_new_user():
    email = request.form.get('email')
    pw = request.form.get('password')
    if not pw or not email:
        flash("missing email or password","danger")

    else:
        # FIXME: validate email with regex

        u = User()
        u.email = email
        u.validated = True
        u.validated_at = datetime.utcnow()
        u.set_password(pw)
        db.session.add(u)

        try:
            db.session.commit()
            flash("user '%s' created" % email,"info")
        except IntegrityError:
            flash("Failed to add user '%s': already exists" % email,"danger")

    return redirect(url_for("users"))


@app.route("/users/set_user_password",methods=["POST"])
def set_user_password():
    user_id = int(request.form.get('user_id'))
    pw = request.form.get('password')
    if not pw:
        flash("missing password","danger")
    else:
        u = User.query.filter_by(user_id=user_id).first()
        if not u:
            flash("invalid user","danger")
        else:
            u.set_password(pw)
            db.session.add(u)
            db.session.commit()
            flash("password for user '%s' updated" % u.email,"info")

    return redirect(url_for("users"))


@app.route("/users/set_user_status",methods=["POST"])
def set_user_status():
    user_id = int(request.form.get('user_id'))
    action = request.form.get('action')
    u = User.query.filter_by(user_id=user_id).first()
    if not u:
        flash("invalid user","danger")
    else:
        if action == "enable":
            u.active = True
        else:
            u.active = False
        db.session.add(u)
        db.session.commit()
        flash("user '%s' updated" % u.email,"info")

    return redirect(url_for("users"))
