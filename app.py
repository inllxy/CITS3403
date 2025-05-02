# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User        # models.py 见下一节
from auth import auth_bp           # 蓝图
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder="Html",        # 直接指向 Html 目录
    static_folder=".",             # 把当前根目录当 static
    static_url_path="/static"      # 浏览器里用 /static/... 访问
)

app.config.update(
    SECRET_KEY="replace-with-random-string",
    SQLALCHEMY_DATABASE_URI="sqlite:///sf6_spotlight.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# --- 数据库与登录管理 ---
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ------------------------

# 注册认证蓝图
app.register_blueprint(auth_bp)

# 首页：直接渲染你原来的主页面
@app.route("/")
def index():
    return render_template("SF6_Competition_Main_Page.html")

# CLI：初始化数据库
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("✔ 数据库已初始化")

if __name__ == "__main__":
    app.run(debug=True)
