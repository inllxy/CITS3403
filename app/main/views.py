from flask import Blueprint, render_template, jsonify
from app.forms import LoginForm, RegisterForm
from app.models import Competition
from app.models import Player

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    competitions = Competition.query.all()
    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template(
        "SF6_Competition_Main_Page.html",
        competitions=competitions,
        login_form=login_form,
        register_form=register_form
    )
@main_bp.route("/players")
def player_page():
    players = Player.query.all()
    return render_template(
        "SF6_Competition_Player_Page.html",
        players=players,
        login_form=LoginForm(),
        register_form=RegisterForm()
    )

@main_bp.route("/bracket/Bracket")
def bracket():
    comp = Competition.query.first()
    return render_template("Bracket.html", comp=comp)

@main_bp.route('/api/competitions', methods=['GET'])
def get_competitions():
    competitions = Competition.query.all()
    return jsonify([{
        'id': comp.id,
        'name': comp.name,
        'bracket': comp.bracket
    } for comp in competitions])