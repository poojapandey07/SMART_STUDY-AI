import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models import User, Achievement
from backend.database.database import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student account."""
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    university = data.get('university', 'Stanford University').strip()
    major = data.get('major', 'Computer Science & AI').strip()

    # Validation
    if not name:
        return jsonify({'success': False, 'message': 'Name is required'}), 400
    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({'success': False, 'message': 'A valid email address is required'}), 400
    if not password or len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'}), 400

    # Check for existing user
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'An account with this email already exists'}), 400

    # Create User
    new_user = User(
        name=name,
        email=email,
        university=university,
        major=major,
        study_goal_hours=5.0,
        streak=1
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    # Seed default starter achievement
    starter_ach = Achievement(
        user_id=new_user.id,
        badge_key="welcome",
        title="Smart Learner",
        description="Created your SmartStudy AI account",
        icon="🚀",
        unlocked=True,
        progress_text="Unlocked"
    )
    db.session.add(starter_ach)
    db.session.commit()

    # Generate JWT token (identity = user.id as string)
    token = create_access_token(identity=str(new_user.id))

    return jsonify({
        'success': True,
        'message': 'Account registered successfully',
        'data': {
            'user': new_user.to_dict(),
            'token': token
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate student with email and password."""
    data = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {
            'user': user.to_dict(),
            'token': token
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Retrieve currently authenticated user's profile."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    return jsonify({
        'success': True,
        'message': 'User profile retrieved',
        'data': {
            'user': user.to_dict()
        }
    }), 200
