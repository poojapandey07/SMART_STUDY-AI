from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.services.progress_service import ProgressService

progress_bp = Blueprint('progress', __name__, url_prefix='/api/progress')

@progress_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_progress_dashboard():
    """Retrieve core progress KPIs for student dashboard."""
    user_id = int(get_jwt_identity())
    metrics = ProgressService.get_dashboard_metrics(user_id)

    return jsonify({
        'success': True,
        'message': 'Dashboard progress metrics calculated',
        'data': metrics
    }), 200


@progress_bp.route('/weekly', methods=['GET'])
@jwt_required()
def get_weekly_progress():
    """Retrieve daily study hour breakdown for the current week."""
    user_id = int(get_jwt_identity())
    weekly = ProgressService.get_weekly_breakdown(user_id)

    return jsonify({
        'success': True,
        'message': 'Weekly study breakdown calculated',
        'data': {
            'weekly_hours': weekly
        }
    }), 200


@progress_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subject_mastery():
    """Retrieve subject-wise mastery calculations."""
    user_id = int(get_jwt_identity())
    subjects = ProgressService.get_subject_progress(user_id)

    return jsonify({
        'success': True,
        'message': 'Subject mastery progress calculated',
        'data': {
            'subjects': subjects
        }
    }), 200
