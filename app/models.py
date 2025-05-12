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
    name = db.Column(db.String(100), nullable=False)               # Competition name
    year = db.Column(db.Integer, nullable=False)                   # Year
    month = db.Column(db.String(10), nullable=False)               # Month abbreviation
    day = db.Column(db.Integer, nullable=False)                    # Day of the month
    poster_url = db.Column(db.String(255))                         # Poster image or link
    logo_url = db.Column(db.String(255))                           # Competition logo
    comp_link = db.Column(db.String(255))                          # External competition link
    visibility = db.Column(db.String(20), default='public')        # private/public visibility
    bracket = db.Column(db.JSON)                                   # Bracket structure
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    league = db.Column(db.String(100))                      # League name
    twitter = db.Column(db.String(255))                     # Twitter profile link
    twitch = db.Column(db.String(255))                      # Twitch profile link
    visibility = db.Column(db.String(20), default="public") # Player visibility (public/private)
    photo_url = db.Column(db.String(255))                   # Path or link to player photo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)