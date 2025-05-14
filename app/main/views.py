from flask import Blueprint, render_template
from app.forms import LoginForm, RegisterForm
from app.models import Competition

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    competitions = Competition.query.all()
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template(
        "SF6_Competition_Main_Page.html",
        competitions=competitions,
        login_form=login_form,
        register_form=register_form
    )
