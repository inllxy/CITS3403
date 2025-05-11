# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")   # user / admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)               # 比赛名称
    year = db.Column(db.Integer, nullable=False)                   # 年份
    month = db.Column(db.String(10), nullable=False)               # 月份缩写
    day = db.Column(db.Integer, nullable=False)                    # 日期（几号）
    poster_url = db.Column(db.String(255))                         # 结果图或链接
    logo_url = db.Column(db.String(255))                           # 比赛 logo
    comp_link = db.Column(db.String(255))                          # 比赛外链
    visibility = db.Column(db.String(20), default='public')        # private/public
    bracket = db.Column(db.JSON)                                   # 对战表结构
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    badge = db.Column(db.String(50))                   # 对应 player-badge 的内容
    img_url = db.Column(db.String(255))                # 对应 player-img 的 src
    event_line1 = db.Column(db.String(255))            # 对应 event-line1
    event_line2 = db.Column(db.String(255))            # 对应 event-line2
    social_links = db.Column(db.Text)                  # 存 JSON 字符串或 HTML 片段都行
    created_at = db.Column(db.DateTime, default=datetime.utcnow)