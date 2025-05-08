# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import calendar

# 全局对象
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = None  # 供 flask db 使用

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",   # 确保 templates/ 是你的 HTML 目录
        static_folder="static"        # static 文件夹
    )
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 初始化迁移工具
    global migrate
    migrate = Migrate(app, db)

    # 导入模型（必要，否则无法识别模型）
    from . import models

    # 注册认证蓝图
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # ========== 路由区域 ==========

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

    return app
