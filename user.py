import os
import calendar
from flask import Flask, request, redirect, send_from_directory, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flask import jsonify

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')
app.secret_key = 'replace-with-a-secure-secret'

comments_by_competition = {}  # key: competition index or name, value: list of comments


# serve anything under the css/ folder via /css/<filename>
@app.route('/static/css/user.css')
def css(filename):
    css_dir = os.path.join(app.root_path, 'css')
    return send_from_directory(css_dir, filename)

# serve anything under the js/ folder via /js/<filename>
@app.route('/static/js/<path:filename>')
def static_js(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'JavaScript'), filename)


# make Python calendar module available in Jinja
app.jinja_env.globals['calendar'] = calendar

# ensure upload folder exists
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# allowed file types for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In-memory stores
competitions = []
players = []

@app.route('/')
def user_page():
    # pass both competitions and players to the template
    return render_template('user_page.html',
                           competitions=competitions,
                           players=players)
#The form sends the player's data (name, league, image, social links, visibility) to the server.
@app.route('/submit-player', methods=['POST'])
def submit_player():
    # Photo (file vs link)
    photo_file = request.files.get('photo_file')
    if photo_file and allowed_file(photo_file.filename):
        fn = secure_filename(photo_file.filename)
        photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        photo_url = url_for('static', filename=f'uploads/{fn}')
    else:
        photo_url = request.form.get('photo_link') or ''

    # Other fields
    name    = request.form['player_name']
    league  = request.form['league']
    twitter = request.form.get('twitter_link') or ''
    twitch  = request.form.get('twitch_link') or ''
    visibility = request.form['visibility']

    players.append({
        'photo_url': photo_url,
        'name': name,
        'league': league,
        'twitter': twitter,
        'twitch': twitch,
        'visibility': visibility
    })

    flash(f'Player “{name}” added ({visibility}).', 'success')
    return redirect(url_for('user_page'))

@app.route('/submit-competition', methods=['POST'])
def submit_competition():
    # (your existing competition logic unchanged)...
    name       = request.form['name']
    year       = request.form['year']
    month      = int(request.form['month'])
    date       = request.form['date']
    comp_link  = request.form['comp_link']
    visibility = request.form['visibility']

    # Poster
    poster_file = request.files.get('poster_file')
    if poster_file and allowed_file(poster_file.filename):
        fn = secure_filename(poster_file.filename)
        poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        poster_url = url_for('static', filename=f'uploads/{fn}')
    else:
        poster_url = request.form.get('poster_link') or ''

    # Logo
    logo_file = request.files.get('logo_file')
    if logo_file and allowed_file(logo_file.filename):
        fn = secure_filename(logo_file.filename)
        logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        logo_url = url_for('static', filename=f'uploads/{fn}')
    else:
        logo_url = request.form.get('logo_link') or ''

    # Bracket parsing...
    raw = {k:v for k,v in request.form.items() if k.startswith('round')}
    bracket = {}
    for key, val in raw.items():
        parts = key.split('_')
        r = int(parts[0].replace('round',''))
        m = int(parts[1].replace('match',''))
        p = int(parts[2].replace('player',''))
        bracket.setdefault(r, {}).setdefault(m, {})[p] = val
    bracket_data = {
      r: [ (pair[1], pair[2]) for m,pair in sorted(matches.items()) ]
      for r, matches in bracket.items()
    }

    month_abbr = calendar.month_abbr[month].upper() + '.'

    competitions.append({
      'name': name,
      'year': year,
      'month': month_abbr,
      'date': date,
      'poster_url': poster_url,
      'logo_url': logo_url,
      'comp_link': comp_link,
      'visibility': visibility,
      'bracket': bracket_data
    })
    return redirect(url_for('user_page'))


@app.route('/api/comment', methods=['POST'])
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

    flash(f'“{name}” saved ({visibility}).', 'success')
    return redirect(url_for('user_page'))
likes_by_competition = {}

@app.route('/api/like', methods=['POST'])
def like():
    data = request.json
    comp_id = data.get('comp_id')
    if not comp_id:
        return jsonify({'error': 'Missing comp_id'}), 400

    likes_by_competition[comp_id] = likes_by_competition.get(comp_id, 0) + 1
    return jsonify({'likes': likes_by_competition[comp_id]})


if __name__ == '__main__':
    app.run(debug=True)