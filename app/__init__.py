# app/__init__.py
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from .forms import LoginForm, RegisterForm
import calendar



# Global instances
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = None  # Used by flask-migrate

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",   # Folder for HTML templates
        static_folder="static"         # Folder for static files like CSS, JS, images
    )
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    # Set up migration engine
    global migrate
    migrate = Migrate(app, db)

    # Import models so they are registered with SQLAlchemy
    from . import models

    # Register authentication blueprint
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    # Register user blueprint
    from .user.views import user_bp
    app.register_blueprint(user_bp, url_prefix='/dashboard')

    from .main.views import main_bp   # 🔁 移动到这里
    app.register_blueprint(main_bp)

    # ========== Application Routes ==========

    @app.route("/")
    def index():
        from app.models import Competition
        competitions = Competition.query.all()
        login_form = LoginForm()
        register_form = RegisterForm()
        return render_template(
            "SF6_Competition_Main_Page.html",
            login_form=login_form,
            register_form=register_form,
            competitions=competitions,
            
        )

    @app.route("/players")
    def player_page():
        return render_template("SF6_Competition_Player_Page.html")

    @app.route("/bracket/Bracket")
    def bracket():
    # 假设你想从数据库里取一个 competition 对象
        from app.models import Competition
        comp = Competition.query.first()  # 或者根据某个 ID 获取

        return render_template("Bracket.html", comp=comp)

    
    # --- ALIAS for auth.py’s redirect(url_for("user_dashboard")) ---
    @app.route("/dashboard", endpoint="user_dashboard")
    def _dashboard_alias():
        # redirect to the real dashboard view at /dashboard/
        return redirect(url_for("user.user_page"))

    # Callback to load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Delayed import to avoid circular dependency
        return User.query.get(int(user_id))

    return app
