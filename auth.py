# auth.py
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from email_validator import validate_email, EmailNotValidError
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    u = request.form["username"].strip()
    e = request.form["email"].strip().lower()
    p = request.form["password"]

    if User.query.filter((User.username == u) | (User.email == e)).first():
        flash("The username or email already exists", "error")
        return redirect(url_for("index"))

    try:
        validate_email(e, check_deliverability=False)
    except EmailNotValidError:
        flash("The email format is incorrect", "error")
        return redirect(url_for("index"))

    user = User(username=u, email=e)
    user.set_password(p)
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in", "success")
    return redirect(url_for("index"))

@auth_bp.route("/login", methods=["POST"])
def login():
    u = request.form["username"].strip()
    p = request.form["password"]
    user = (User.query.filter_by(username=u).first() or
            User.query.filter_by(email=u.lower()).first())
    if user and user.check_password(p):
        login_user(user)
        flash("Login successful", "success")
        return redirect(url_for("user_dashboard"))  # Redirect to a user dashboard or main page
    else:
        flash("Incorrect account or password", "error")
        return redirect(url_for("index"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out of the system", "success")
    return redirect(url_for("index"))
