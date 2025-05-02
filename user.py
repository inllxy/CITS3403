import os
import calendar
from flask import Flask, request, redirect, send_from_directory, url_for, flash, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__,
            template_folder='html',
            static_folder='static')
app.secret_key = 'replace-with-a-secure-secret'
# serve anything under the css/ folder via /css/<filename>
@app.route('/css/<path:filename>')
def css(filename):
    css_dir = os.path.join(app.root_path, 'css')
    return send_from_directory(css_dir, filename)

app.jinja_env.globals['calendar'] = calendar

# ensure upload folder exists
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In-memory store
competitions = []

@app.route('/')
def user_page():
    # pass all comps to the template
    return render_template('user_page.html', competitions=competitions)

@app.route('/main')
def main_page():
    return render_template('SF6_Competition_Main_Page.html')

@app.route('/submit-competition', methods=['POST'])
def submit_competition():
    # gather text fields
    name       = request.form['name']
    year       = request.form['year']
    month      = int(request.form['month'])
    date       = request.form['date']
    comp_link  = request.form['comp_link']
    visibility = request.form['visibility']

    # poster upload vs URL
    poster_file = request.files.get('poster_file')
    if poster_file and allowed_file(poster_file.filename):
        fn = secure_filename(poster_file.filename)
        poster_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        poster_url = url_for('static', filename=f'uploads/{fn}')
    else:
        poster_url = request.form.get('poster_link') or ''

    # logo upload vs URL
    logo_file = request.files.get('logo_file')
    if logo_file and allowed_file(logo_file.filename):
        fn = secure_filename(logo_file.filename)
        logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        logo_url = url_for('static', filename=f'uploads/{fn}')
    else:
        logo_url = request.form.get('logo_link') or ''

    # bracket inputs
    raw = {k:v for k,v in request.form.items() if k.startswith('round')}
    # organize into { round: [ (p1,p2), ... ] }
    bracket = {}
    for key, val in raw.items():
        # key format: round{r}_match{m}_player{p}
        parts = key.split('_')
        r = int(parts[0].replace('round',''))
        m = int(parts[1].replace('match',''))
        p = int(parts[2].replace('player',''))
        bracket.setdefault(r, {}).setdefault(m, {})[p] = val
    # convert inner dict to tuples
    bracket_data = {
      r: [ (pair[1], pair[2]) for m,pair in sorted(matches.items()) ]
      for r, matches in bracket.items()
    }

    # store month abbr
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

    flash(f'“{name}” saved ({visibility}).', 'success')
    return redirect(url_for('user_page'))

if __name__ == '__main__':
    app.run(debug=True)
