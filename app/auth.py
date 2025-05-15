from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from email_validator import validate_email, EmailNotValidError
from .models import db, User
from .forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = form.username.data.strip()
        e = form.email.data.strip().lower()
        p = form.password.data

        if User.query.filter((User.username == u) | (User.email == e)).first():
            flash("The username or email already exists", "error")
            return redirect(url_for("auth.register"))

        try:
            validate_email(e, check_deliverability=False)
        except EmailNotValidError:
            flash("The email format is incorrect", "error")
            return redirect(url_for("auth.register"))

        user = User(username=u, email=e)
        user.set_password(p)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in", "success")
        return redirect(url_for("main.index"))

    return redirect(url_for("main.index"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = form.username.data.strip()
        p = form.password.data
        user = User.query.filter_by(username=u).first() or User.query.filter_by(email=u.lower()).first()
        if user and user.check_password(p):
            login_user(user)
            flash("Login successful", "success")
            return redirect(url_for("user.user_page"))  # 改为你 Blueprint 里的 dashboard 页面
        else:
            flash("Incorrect account or password", "error")

    return redirect(url_for("main.index"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out of the system", "success")
    return redirect(url_for("main.index"))
