# routes/tournament.py
from flask import Blueprint, request, jsonify, abort
from login import db
from models import User, Tournament, Match
import csv
from io import StringIO

# routes/tournament.py
# This file contains the routes for tournament management, including uploading CSV files, viewing tournaments, and sharing them with other users.
tournament_bp = Blueprint('tournament', __name__)

def get_current_user():
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    user = User.verify_token(token)
    if not user:
        abort(401, 'Invalid or expired token')
    return user

@tournament_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user = get_current_user()
    own = Tournament.query.filter_by(owner_id=user.id).all()
    shared = user.shared_tournaments
    return jsonify({
        'own': [{'id': t.id, 'name': t.name} for t in own],
        'shared': [{'id': t.id, 'name': t.name} for t in shared]
    })

@tournament_bp.route('/upload', methods=['POST'])
def upload():
    user = get_current_user()
    name = request.form.get('name')
    file = request.files.get('file')
    if not name or not file:
        abort(400, 'Tournament name and CSV file required')
    # Create tournament
    tourn = Tournament(name=name, owner_id=user.id)
    db.session.add(tourn)
    db.session.commit()
    # Parse CSV stream
    stream = StringIO(file.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    for row in reader:
        m = Match(
            tournament_id=tourn.id,
            player_a=row['player_a'],
            score_a=int(row.get('score_a', 0)),
            player_b=row['player_b'],
            score_b=int(row.get('score_b', 0))
        )
        db.session.add(m)
    db.session.commit()
    return jsonify({'message': 'Uploaded', 'tournament_id': tourn.id})

@tournament_bp.route('/<int:tourn_id>', methods=['GET'])
def view_tournament(tourn_id):
    user = get_current_user()
    tourn = Tournament.query.get_or_404(tourn_id)
    if tourn.owner_id != user.id and user not in tourn.shared_tournaments:
        abort(403)
    # Compute simple win-count stats
    stats = {}
    for m in tourn.matches:
        stats.setdefault(m.player_a, 0)
        stats.setdefault(m.player_b, 0)
        if m.score_a > m.score_b:
            stats[m.player_a] += 1
        if m.score_b > m.score_a:
            stats[m.player_b] += 1
    return jsonify({'tournament': {'id': tourn.id, 'name': tourn.name}, 'stats': stats})

@tournament_bp.route('/<int:tourn_id>/share', methods=['POST'])
def share_tournament(tourn_id):
    user = get_current_user()
    tourn = Tournament.query.get_or_404(tourn_id)
    if tourn.owner_id != user.id:
        abort(403)
    user_ids = request.json.get('user_ids', [])
    users = User.query.filter(User.id.in_(user_ids)).all()
    tourn.shared_tournaments = users
    db.session.commit()
    return jsonify({'message': 'Share settings updated'})
