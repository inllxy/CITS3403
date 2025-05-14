from flask import Blueprint, render_template
from app.models import Player

player_bp = Blueprint("player", __name__, url_prefix="/players")

@player_bp.route("/")
def player_page():
    players = Player.query.all()
    return render_template("SF6_Competition_Player_Page.html", players=players)
