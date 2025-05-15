# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
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
    
shared_competitions = db.Table(
    'shared_competitions',
    db.Column('competition_id', db.Integer, db.ForeignKey('competitions.id'), primary_key=True),
    db.Column('shared_with_user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
    
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
    user_id = db.Column(db.Integer, ForeignKey('users.id', name='fk_competitions_users'), nullable=False)
    user = relationship('User', backref='competitions')
    shared_with = db.relationship(
        'User',
        secondary=shared_competitions,
        backref='shared_competitions'
    )
    
shared_players = db.Table(
    'shared_players',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('shared_with_user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)    
    
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
    user_id = db.Column(db.Integer, ForeignKey('users.id', name='fk_players_users'), nullable=False)
    user = relationship('User', backref='players')
    shared_with = db.relationship(
    'User',
    secondary=shared_players,
    backref='shared_players'
)

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='comments')
    competition = db.relationship('Competition', backref='comments')


# models.py

