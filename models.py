# models.py
<<<<<<< Updated upstream
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

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
=======

import jwt, datetime
from flask_login import UserMixin
from login import db, app  # or from your app import db, app

# association table for sharing
shared = db.Table(
    'shared',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password      = db.Column(db.String(200), nullable=False)
    role          = db.Column(db.String(20), default='user')

    # relationships
    tournaments        = db.relationship('Tournament', backref='owner', lazy=True)
    shared_tournaments = db.relationship(
        'Tournament', secondary=shared,
        backref=db.backref('shared_with_users', lazy='dynamic')
    )

    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'role': self.role
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except:
            return None

    @staticmethod
    def verify_admin(token):
        u = User.verify_token(token)
        return u if u and u.role == 'admin' else None

class Tournament(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    matches  = db.relationship('Match', backref='tournament', lazy=True)

class Match(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    player_a      = db.Column(db.String(100), nullable=False)
    score_a       = db.Column(db.Integer, nullable=False)
    player_b      = db.Column(db.String(100), nullable=False)
    score_b       = db.Column(db.Integer, nullable=False)
>>>>>>> Stashed changes
