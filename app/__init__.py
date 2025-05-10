# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
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

    # Set up migration engine
    global migrate
    migrate = Migrate(app, db)

    # Import models so they are registered with SQLAlchemy
    from . import models

    # Register authentication blueprint
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    # Register user blueprint
    from .user.route import user_bp
    app.register_blueprint(user_bp)


    # ========== Application Routes ==========

    @app.route("/")
    def index():
        return render_template("SF6_Competition_Main_Page.html")

    @app.route("/dashboard")
    
    def user_dashboard():
        return render_template("user_page.html", competitions=[], players=[], calendar=calendar)

    @app.route("/players")
    def player_page():
        return render_template("SF6_Competition_Player_Page.html")

    @app.route("/bracket/<name>")
    def bracket(name):
        return render_template(f"{name}.html")

    # Callback to load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Delayed import to avoid circular dependency
        return User.query.get(int(user_id))

    return app
