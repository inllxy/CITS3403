# app/user/views.py
import os
import calendar
from flask import Blueprint, request, redirect, send_from_directory, url_for, flash, render_template, jsonify
from werkzeug.utils import secure_filename

user_bp = Blueprint('user', __name__, template_folder='../templates', static_folder='../static')

# Global in-memory stores
competitions = []
players = []
comments_by_competition = {}
likes_by_competition = {}

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Calendar in Jinja
@user_bp.app_context_processor
def inject_calendar():
    return dict(calendar=calendar)

@user_bp.route('/')
def user_page():
    return render_template("user_page.html", competitions=[], players=[])

@user_bp.route('/submit-player', methods=['POST'])

def submit_player():
    print("--- FORM DATA ---")
    print(request.form)
    print("--- FILES ---")
    print(request.files)

    photo_file = request.files.get('photo_file')
    if photo_file and allowed_file(photo_file.filename):
        fn = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(UPLOAD_FOLDER, fn))
        photo_url = url_for('static', filename=f'uploads/{fn}')
    else:
        photo_url = request.form.get('photo_link') or ''

    players.append({
        'photo_url': photo_url,
        'name': request.form['player_name'],
        'league': request.form['league'],
        'twitter': request.form.get('twitter_link') or '',
        'twitch': request.form.get('twitch_link') or '',
        'visibility': request.form['visibility']
    })

    
    return redirect(url_for('user.user_page'))

@user_bp.route('/submit-competition', methods=['POST'])
def submit_competition():
    name = request.form['name']
    year = request.form['year']
    month = int(request.form['month'])
    date = request.form['date']
    comp_link = request.form['comp_link']
    visibility = request.form['visibility']

    # Poster
    poster_file = request.files.get('poster_file')
    if poster_file and allowed_file(poster_file.filename):
        fn = secure_filename(poster_file.filename)
        poster_file.save(os.path.join(UPLOAD_FOLDER, fn))
        poster_url = url_for('static', filename=f'uploads/{fn}')
    else:
        poster_url = request.form.get('poster_link') or ''

    # Logo
    logo_file = request.files.get('logo_file')
    if logo_file and allowed_file(logo_file.filename):
        fn = secure_filename(logo_file.filename)
        logo_file.save(os.path.join(UPLOAD_FOLDER, fn))
        logo_url = url_for('static', filename=f'uploads/{fn}')
    else:
        logo_url = request.form.get('logo_link') or ''

    raw = {k: v for k, v in request.form.items() if k.startswith('round')}
    bracket = {}
    for key, val in raw.items():
        r, m, p = map(int, [key.replace('round', '').split('_')[0],
                            key.split('_')[1].replace('match', ''),
                            key.split('_')[2].replace('player', '')])
        bracket.setdefault(r, {}).setdefault(m, {})[p] = val

    bracket_data = {
        r: [(pair[1], pair[2]) for m, pair in sorted(matches.items())]
        for r, matches in bracket.items()
    }

    competitions.append({
        'name': name,
        'year': year,
        'month': calendar.month_abbr[month].upper() + '.',
        'date': date,
        'poster_url': poster_url,
        'logo_url': logo_url,
        'comp_link': comp_link,
        'visibility': visibility,
        'bracket': bracket_data
    })

    return redirect(url_for('user.user_page'))

@user_bp.route('/api/comment', methods=['POST'])
def add_comment():
    data = request.json
    comp_id = data.get('comp_id')
    text = data.get('text')

    if not comp_id or not text:
        return jsonify({'error': 'Missing comp_id or text'}), 400

    comments_by_competition.setdefault(comp_id, []).append(text)
    return jsonify({
        'count': len(comments_by_competition[comp_id]),
        'comments': comments_by_competition[comp_id]
    })

@user_bp.route('/api/like', methods=['POST'])
def like():
    data = request.json
    comp_id = data.get('comp_id')
    if not comp_id:
        return jsonify({'error': 'Missing comp_id'}), 400

    likes_by_competition[comp_id] = likes_by_competition.get(comp_id, 0) + 1
    return jsonify({'likes': likes_by_competition[comp_id]})
