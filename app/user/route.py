# app/user/views.py
import os
import uuid
import calendar
from flask import (
    Blueprint, current_app, request,
    redirect, url_for, flash,
    render_template, jsonify
)
from flask_login import current_user
from werkzeug.utils import secure_filename

user_bp = Blueprint(
    'user', __name__,
    template_folder='../templates',
    static_folder='../static',
    static_url_path='/static'
)

# In-memory stores
competitions = []
players = []
comments_by_competition = {}
likes_by_competition = {}
shared_players = {}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def save_file(file_storage):
    """
    Save an uploaded FileStorage into
    static/uploads with a UUID name, return its URL.
    """
    ext = os.path.splitext(file_storage.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    upload_dir = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    dest = os.path.join(upload_dir, secure_filename(unique_name))
    file_storage.save(dest)
    return url_for('static', filename=f'uploads/{unique_name}')

@user_bp.app_context_processor
def inject_calendar():
    return {'calendar': calendar}

@user_bp.route('/')
def user_page():
    me = current_user.username
    mine = players[:]                          # your own
    mine.extend(shared_players.get(me, []))    # plus any shared with me
    return render_template(
        'user_page.html',
         competitions=competitions,
         players=mine
    )
    
@user_bp.route('/submit-player', methods=['POST'])
def submit_player():
    # Handle photo upload or link
    photo = request.files.get('photo_file')
    if photo and allowed_file(photo.filename):
        photo_url = save_file(photo)
    else:
        photo_url = request.form.get('photo_link', '')

    # Build the player dictionary
    player = {
        'photo_url':  photo_url,
        'name':       request.form.get('player_name', '').strip(),
        'league':     request.form.get('league', '').strip(),
        'twitter':    request.form.get('twitter_link', '').strip(),
        'twitch':     request.form.get('twitch_link', '').strip(),
        'visibility': request.form.get('visibility', 'public'),
        'owner':      current_user.username,
        'shared_with': []  # Will be populated if shared
    }

    # Check if the action is "share"
    action = request.form.get('action', 'public')
    if action == 'share':
        # Get the list of recipients
        raw = request.form.get('share_with', '')
        recipients = [u.strip() for u in raw.split(',') if u.strip()]
        player['shared_with'] = recipients
        # still save to my own dashboard
        players.append(player)
        # Save the player to each recipient's dashboard
        for u in recipients:
            shared_players.setdefault(u, []).append(player.copy())

        flash(f"Player shared with: {', '.join(recipients)}", 'success')
    else:
        # Save the player to the current user's dashboard
        players.append(player)
        flash('Player added successfully.', 'success')

    return redirect(url_for('user.user_page'))

# new global for tracking shared-to lists
shared_competitions = {}  # key: username, value: list of competition dicts

@user_bp.route('/submit-competition', methods=['POST'])
def submit_competition():
    # 1) Read the form
    name       = request.form.get('name', '').strip()
    year       = request.form.get('year', '').strip()
    month_idx  = int(request.form.get('month', 0))
    date       = request.form.get('date', '').strip()
    comp_link  = request.form.get('comp_link', '').strip()
    action     = request.form.get('action', 'public')  
    #    ↑ this replaces your old 'visibility'
    action    = request.form['action']  # "public", "private", or "share"
    # 2) Handle files as before
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

    # 3) Parse **all** bracket inputs
    raw = {k: v for k, v in request.form.items() if k.startswith('round')}
    bracket = {}
    for key, val in raw.items():
        # key looks like "round{r}_match{m}_{field}{i}"
        # e.g. "round1_match3_team2", "round2_match5_score1", etc.
        parts = key.split('_')            # => ["round1","match3","team2"]
        r     = int(parts[0].replace('round',''))
        m     = int(parts[1].replace('match',''))
        field = parts[2]                  # e.g. "team2", "player1", "score1"
        bracket.setdefault(r, {})\
            .setdefault(m, {})[field] = val

    # 4) Turn that nested dict into a list-of-dicts per round
    bracket_data = {
        r: [
            {
            'team1':   info.get('team1', ''),
            'player1': info.get('player1', ''),
            'score1':  info.get('score1', ''),
            'team2':   info.get('team2', ''),
            'player2': info.get('player2', ''),
            'score2':  info.get('score2', ''),
            # optionally flags if you collected them:
            'flag1_url': info.get('flag1_url',''),
            'flag2_url': info.get('flag2_url',''),
            }
            for m, info in sorted(matches.items())
        ]
        for r, matches in bracket.items()
    }

    # 4) Build our competition dict
    comp = {
        'name':       name,
        'year':       year,
        'month':      calendar.month_abbr[month_idx].upper() + '.',
        'date':       date,
        'poster_url': poster_url,
        'logo_url':   logo_url,
        'comp_link':  comp_link,
        'visibility': action,
        'bracket':    bracket_data,
        'owner':      current_user.username,
        'shared_with': []   # will fill below if needed
    }

    # 5) Branch on action
    if action == 'share':
    # get the text, split by commas, strip whitespace
        raw = request.form.get('share_with', '')
        recipients = [u.strip() for u in raw.split(',') if u.strip()]
        comp['shared_with'] = recipients

        for u in recipients:
            shared_competitions.setdefault(u, []).append(comp)
            # still save to my own dashboard
            competitions.append(comp)
        flash(f"Competition shared with: {', '.join(recipients)}", 'success')
    else:
        competitions.append(comp)
        flash('Competition added successfully.', 'success')


    return redirect(url_for('user.user_page'))


@user_bp.route('/api/comment', methods=['POST'])
def add_comment():
    data = request.get_json() or {}
    # cast comp_id reliably
    try:
        comp_id = int(data['comp_id'])
        text    = data['text'].strip()
        if not text:
            raise ValueError
    except (KeyError, ValueError):
        return jsonify(error='Invalid comp_id or empty text'), 400

    comments_by_competition.setdefault(comp_id, []).append(text)
    return jsonify(
        count    = len(comments_by_competition[comp_id]),
        comments = comments_by_competition[comp_id]
    )

@user_bp.route('/api/like', methods=['POST'])
def like():
    data = request.get_json() or {}
    try:
        comp_id = int(data['comp_id'])
    except (KeyError, ValueError):
        return jsonify(error='Invalid comp_id'), 400

    likes_by_competition[comp_id] = likes_by_competition.get(comp_id, 0) + 1
    return jsonify(likes=likes_by_competition[comp_id])
