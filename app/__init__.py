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

    from .main.views import main_bp 
    app.register_blueprint(main_bp)

    from .playercard.views import player_bp
    app.register_blueprint(player_bp)
    # ========== Application Routes ==========
    
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
