# app/user/views.py
import os
import uuid
import calendar
from flask import (
    Blueprint, current_app, request,
    redirect, url_for, flash,
    render_template, jsonify
)
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
    # Pass the real lists (not empty!) into the template
    return render_template(
        'user_page.html',
        competitions=competitions,
        players=players
    )

@user_bp.route('/submit-player', methods=['POST'])
def submit_player():
    # Handle photo upload or link
    photo = request.files.get('photo_file')
    if photo and allowed_file(photo.filename):
        photo_url = save_file(photo)
    else:
        photo_url = request.form.get('photo_link', '')

    players.append({
        'photo_url':  photo_url,
        'name':       request.form.get('player_name', '').strip(),
        'league':     request.form.get('league', '').strip(),
        'twitter':    request.form.get('twitter_link', '').strip(),
        'twitch':     request.form.get('twitch_link', '').strip(),
        'visibility': request.form.get('visibility', 'public')
    })
    flash('Player added successfully.', 'success')
    return redirect(url_for('user.user_page'))

@user_bp.route('/submit-competition', methods=['POST'])
def submit_competition():
    # Basic form fields
    name       = request.form.get('name', '').strip()
    year       = request.form.get('year', '').strip()
    month_idx  = int(request.form.get('month', 0))
    date       = request.form.get('date', '').strip()
    comp_link  = request.form.get('comp_link', '').strip()
    visibility = request.form.get('visibility', 'public')

    # Poster upload or link
    poster = request.files.get('poster_file')
    if poster and allowed_file(poster.filename):
        poster_url = save_file(poster)
    else:
        poster_url = request.form.get('poster_link', '')

    # Logo upload or link
    logo = request.files.get('logo_file')
    if logo and allowed_file(logo.filename):
        logo_url = save_file(logo)
    else:
        logo_url = request.form.get('logo_link', '')

    # Parse the bracket inputs
    raw = {k: v for k, v in request.form.items() if k.startswith('round')}
    bracket = {}
    for key, val in raw.items():
        # key = "round{r}_match{m}_player{p}"
        r, m, p = map(int, [
            key.replace('round','').split('_')[0],
            key.split('_')[1].replace('match',''),
            key.split('_')[2].replace('player',''),
        ])
        bracket.setdefault(r, {}).setdefault(m, {})[p] = val

    bracket_data = {
        r: [(pair[1], pair[2]) for m, pair in sorted(matches.items())]
        for r, matches in bracket.items()
    }

    competitions.append({
        'name':       name,
        'year':       year,
        'month':      calendar.month_abbr[month_idx].upper() + '.',
        'date':       date,
        'poster_url': poster_url,
        'logo_url':   logo_url,
        'comp_link':  comp_link,
        'visibility': visibility,
        'bracket':    bracket_data
    })
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
