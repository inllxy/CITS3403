# app.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

from models import User
from routes.auth import auth_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# models.py
import jwt
import datetime
from flask_login import UserMixin
from app import db, app

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # user or admin

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
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    @staticmethod
    def verify_admin(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if payload['role'] != 'admin':
                return None
            return User.query.get(payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

# routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Allow optional role assignment

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = user.generate_token()
    return jsonify({'token': token})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    user = User.verify_token(token)
    if not user:
        return jsonify({'message': 'Invalid or expired token'}), 401

    return jsonify({'username': user.username, 'id': user.id, 'role': user.role})

@auth_bp.route('/admin-only', methods=['GET'])
def admin_only():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    user = User.verify_admin(token)
    if not user:
        return jsonify({'message': 'Admins only'}), 403

    return jsonify({'message': f'Welcome, admin {user.username}'})
