# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User        # models.py is shown in the next section
from auth import auth_bp           # Blueprint
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder="Html",        # Directly point to the Html directory
    static_folder="static",        # default static folder
    static_url_path="/static"      # Use /static/... in the browser to access static files
)

app.config.update(
    SECRET_KEY="replace-with-random-string",
    SQLALCHEMY_DATABASE_URI="sqlite:///sf6_spotlight.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# --- Database and login management ---
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ------------------------

# Register the authentication blueprint
app.register_blueprint(auth_bp)

# Homepage: directly render your original main page
@app.route("/")
def index():
    return render_template("SF6_Competition_Main_Page.html")

@app.route("/players")
def player_page():
    return render_template("SF6_Competition_Player_Page.html")

# CLI: initialize the database
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("✔ 数据库已初始化")

if __name__ == "__main__":
    app.run(debug=True)
