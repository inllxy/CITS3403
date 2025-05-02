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
    role     = data.get('role', 'user')
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    hashed = generate_password_hash(password)
    u = User(username=username, password=hashed, role=role)
    db.session.add(u); db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    u = User.query.filter_by(username=data.get('username')).first()
    if not u or not check_password_hash(u.password, data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = u.generate_token()
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
