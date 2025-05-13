# app/user/views.py
import os
import uuid
import calendar
import re
from flask import (
    Blueprint, current_app, request,
    redirect, url_for, flash,
    render_template, jsonify,
    abort
)
from werkzeug.utils import secure_filename
from app.models import db, Competition, Player
from flask_login import login_required, current_user

user_bp = Blueprint(
    'user', __name__,
    template_folder='../templates',
    static_folder='../static',
    static_url_path='/static'
)

@user_bp.app_context_processor
def inject_calendar():
    return {'calendar': calendar}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_file(file_storage):
    ext = os.path.splitext(file_storage.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    upload_dir = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    dest = os.path.join(upload_dir, secure_filename(unique_name))
    file_storage.save(dest)
    return url_for('static', filename=f'uploads/{unique_name}')

@user_bp.route('/')
def user_page():
    competitions = Competition.query.order_by(Competition.created_at.desc()).all()
    players = Player.query.order_by(Player.created_at.desc()).all()
    return render_template('user_page.html', competitions=competitions, players=players)

@user_bp.route('/submit-player', methods=['POST'])
def submit_player():
    photo = request.files.get('photo_file')
    if photo and allowed_file(photo.filename):
        photo_url = save_file(photo)
    else:
        photo_url = request.form.get('photo_link', '')

    player = Player(
        name=request.form.get('player_name', '').strip(),
        league=request.form.get('league', '').strip(),
        twitter=request.form.get('twitter_link', '').strip(),
        twitch=request.form.get('twitch_link', '').strip(),
        visibility=request.form.get('visibility', 'public'),
        photo_url=photo_url
    )
    db.session.add(player)
    db.session.commit()
    flash('Player added successfully.', 'success')
    return redirect(url_for('user.user_page'))

@user_bp.route('/submit-competition', methods=['POST'])
def submit_competition():
    name = request.form.get('name', '').strip()
    year = int(request.form.get('year', 0))
    month_idx = int(request.form.get('month', 0))
    date = int(request.form.get('date', 1))
    comp_link = request.form.get('comp_link', '').strip()
    visibility = request.form.get('visibility', 'public')

    poster = request.files.get('poster_file')
    if poster and allowed_file(poster.filename):
        poster_url = save_file(poster)
    else:
        poster_url = request.form.get('poster_link', '')

    logo = request.files.get('logo_file')
    if logo and allowed_file(logo.filename):
        logo_url = save_file(logo)
    else:
        logo_url = request.form.get('logo_link', '')

    # 1) Collect all input fields related to Rounds/Matches from request.form
    raw = {
        k: v
        for k, v in request.form.items()
        if re.match(r'^round\d+_match\d+_(team|player|score)\d+$', k)
}


    # 2) Temporary storage: bracket_tmp['winner'/'loser'][round_num][match_num][field+idx] = value
    bracket_tmp = {'winner': {}, 'loser': {}}
    for key, val in raw.items():
        # Example key: round1_match3_team2
        m = re.match(
            r'^round(\d+)_match(\d+)_(team|player|score)(\d+)$',
            key
        )
        r, match_no, field, idx = m.groups()
        r, match_no, idx = map(int, (r, match_no, idx))

        # Determine if it belongs to 'winner' or 'loser' based on round number
        # Assume rounds 1~4 are Winner, rounds 5~10 are Loser (based on your HTML)
        bracket_type = 'winner' if r in (1, 2, 3, 4) else 'loser'

        wb = bracket_tmp[bracket_type]
        wb.setdefault(r, {}).setdefault(match_no, {})[f"{field}{idx}"] = val

    # 3) Convert each sub-dictionary into a "list of match dicts", sorted by round and match number
    bracket_data = {}
    for bracket_type, rounds in bracket_tmp.items():
        bracket_data[bracket_type] = {}
        for r_num, matches in sorted(rounds.items()):
            # matches: { match_no: {'team1':..,'player1':..,'score1':.., …}, … }
            bracket_data[bracket_type][r_num] = []
            for m_no, info in sorted(matches.items()):
                # Ensure score strings are converted to integers
                bracket_data[bracket_type][r_num].append({
                    'match': m_no,
                    'team1':   info.get('team1'),
                    'player1': info.get('player1'),
                    'score1':  int(info.get('score1') or 0),
                    'team2':   info.get('team2'),
                    'player2': info.get('player2'),
                    'score2':  int(info.get('score2') or 0),
                })

    new_comp = Competition(
        name=name,
        year=year,
        month=calendar.month_abbr[month_idx].upper() + '.',
        day=date,
        poster_url=poster_url,
        logo_url=logo_url,
        comp_link=comp_link,
        visibility=visibility,
        bracket=bracket_data
    )
    db.session.add(new_comp)
    db.session.commit()
    flash('Competition added successfully.', 'success')
    return redirect(url_for('user.user_page'))

@user_bp.route('/competition/delete/<int:comp_id>', methods=['POST'])
@login_required
def delete_competition(comp_id):
    comp = Competition.query.get_or_404(comp_id)
    db.session.delete(comp)
    db.session.commit()
    flash('The competition has been successfully delected', 'success')
    return redirect(url_for('user_dashboard'))
@user_bp.route('/api/comment', methods=['POST'])

def add_comment():
    data = request.get_json() or {}
    try:
        comp_id = int(data['comp_id'])
        text = data['text'].strip()
        if not text:
            raise ValueError
    except (KeyError, ValueError):
        return jsonify(error='Invalid comp_id or empty text'), 400

    return jsonify(status='ok', message='Comment received (store to DB if needed)')

likes_by_competition = {}

@user_bp.route('/api/like', methods=['POST'])
def like():
    data = request.get_json() or {}
    try:
        comp_id = int(data['comp_id'])
    except (KeyError, ValueError):
        return jsonify(error='Invalid comp_id'), 400

    likes_by_competition[comp_id] = likes_by_competition.get(comp_id, 0) + 1
    return jsonify(likes=likes_by_competition[comp_id])
