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
from app.models import db, Competition, Player, User, shared_players, shared_competitions
from app.models import db, Competition, Player, User, shared_players, shared_competitions
from flask_login import login_required, current_user
from app.forms import CompetitionForm

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
@login_required
def user_page():
    own_comps = Competition.query.filter_by(user_id=current_user.id)

    shared_comps = Competition.query \
        .join(shared_competitions) \
        .filter(shared_competitions.c.shared_with_user_id == current_user.id)

    competitions = own_comps.union(shared_comps) \
        .order_by(Competition.created_at.desc()) \
        .all()

    own_players = Player.query.filter_by(user_id=current_user.id)

    shared_players_query = Player.query \
        .join(shared_players) \
        .filter(shared_players.c.shared_with_user_id == current_user.id)

    players = own_players.union(shared_players_query) \
        .order_by(Player.created_at.desc()) \
        .all()

    own_comps = Competition.query.filter_by(user_id=current_user.id)

    shared_comps = Competition.query \
        .join(shared_competitions) \
        .filter(shared_competitions.c.shared_with_user_id == current_user.id)

    competitions = own_comps.union(shared_comps) \
        .order_by(Competition.created_at.desc()) \
        .all()

    own_players = Player.query.filter_by(user_id=current_user.id)

    shared_players_query = Player.query \
        .join(shared_players) \
        .filter(shared_players.c.shared_with_user_id == current_user.id)

    players = own_players.union(shared_players_query) \
        .order_by(Player.created_at.desc()) \
        .all()
    form = CompetitionForm()
    return render_template('user_page.html', competitions=competitions, players=players, form=form)




@user_bp.route('/submit-player', methods=['POST'])
@login_required
def submit_player():
    photo = request.files.get('photo_file')
    if photo and allowed_file(photo.filename):
        photo_url = save_file(photo)
    else:
        photo_url = request.form.get('photo_link', '')

    action = request.form.get('action', 'public')  
    if action == 'private':
        visibility = 'private'
    elif action == 'share':
        visibility = 'shared'
    else:
        visibility = 'public'

    action = request.form.get('action', 'public')  
    if action == 'private':
        visibility = 'private'
    elif action == 'share':
        visibility = 'shared'
    else:
        visibility = 'public'

    player = Player(
        name=request.form.get('player_name', '').strip(),
        league=request.form.get('league', '').strip(),
        twitter=request.form.get('twitter_link', '').strip(),
        twitch=request.form.get('twitch_link', '').strip(),
        visibility=visibility,
        photo_url=photo_url,
        user_id=current_user.id
    )
    if action == 'share':
        usernames = request.form.get('share_with', '')
        username_list = [u.strip() for u in usernames.split(',') if u.strip()]
        for uname in username_list:
            user = User.query.filter_by(username=uname).first()
            if user:
                player.shared_with.append(user)

    if action == 'share':
        usernames = request.form.get('share_with', '')
        username_list = [u.strip() for u in usernames.split(',') if u.strip()]
        for uname in username_list:
            user = User.query.filter_by(username=uname).first()
            if user:
                player.shared_with.append(user)

    db.session.add(player)
    db.session.commit()
    flash('Player added successfully.', 'success')
    return redirect(url_for('user.user_page'))



@user_bp.route('/submit-competition', methods=['POST'])
@login_required
def submit_competition():
    name = request.form.get('name', '').strip()
    year = int(request.form.get('year', 0))
    month_idx = int(request.form.get('month', 0))
    date = int(request.form.get('date', 1))
    comp_link = request.form.get('comp_link', '').strip()
    action = request.form.get('action', 'public')
    action = request.form.get('action', 'public')

    if action == 'private':
        visibility = 'private'
    elif action == 'share':
        visibility = 'shared'
    else:
        visibility = 'public'
    if action == 'private':
        visibility = 'private'
    elif action == 'share':
        visibility = 'shared'
    else:
        visibility = 'public'

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
        bracket=bracket_data,
        user_id=current_user.id
    )
    db.session.add(new_comp)

    if action == 'share':
        usernames = request.form.get("share_with", "")
        username_list = [u.strip() for u in usernames.split(",") if u.strip()]
        for uname in username_list:
            user = User.query.filter_by(username=uname).first()
            if user:
                new_comp.shared_with.append(user)


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

@user_bp.route('/player/delete/<int:player_id>', methods=['POST'])
@login_required
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    flash(f'Player "{player.name}" deleted', 'success')
    return redirect(url_for('user.user_page'))

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

@user_bp.route('/share-player/<int:player_id>', methods=['POST'])
@login_required
def share_player(player_id):
    usernames = request.form.get("share_with", "")  # e.g. "alice,bob"
    username_list = [u.strip() for u in usernames.split(",") if u.strip()]

    player = Player.query.get_or_404(player_id)

    if player.user_id != current_user.id:
        abort(403)


    for uname in username_list:
        user = User.query.filter_by(username=uname).first()
        if user:
            player.shared_with.append(user)
    player.visibility = 'shared'
    db.session.commit()
    flash("Player shared successfully.", "success")
    return redirect(url_for("user.user_page"))

@user_bp.route('/competition/<int:comp_id>/share', methods=['POST'])
@login_required
def share_competition(comp_id):
    # 1) 拿到用户名列表
    raw = request.form.get('share_with','')
    names = [n.strip() for n in raw.split(',') if n.strip()]
    if not names:
        flash('请输入至少一个用户名','warning')
        return redirect(url_for('user.user_dashboard'))

    # 2) 循环查用户，插入 shared_competitions
    for name in names:
        user = User.query.filter_by(username=name).first()

        share = shared_competitions(
            competition_id=comp_id,
            shared_with_user_id=user.id
        )
        db.session.add(share)

    db.session.commit()
    flash('分享邀请已发送！','success')
    return redirect(url_for('user.user_dashboard'))