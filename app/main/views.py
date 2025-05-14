# 假设在 app/main/views.py 或 app/routes.py

from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Competition  # 确保导入你定义的 Competition 模型

main_bp = Blueprint('main', __name__)

@main_bp.route("/")  # 首页路由
@login_required  # 如果首页需要登录才能访问
def home():
    competitions = Competition.query.all()  # 查询所有比赛记录
    return render_template("SF6_Competition_Main_Page.html", competitions=competitions)
