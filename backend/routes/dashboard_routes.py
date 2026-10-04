from datetime import datetime
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Task, StudySchedule, StudySession, Quiz
from backend.services.progress_service import ProgressService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('', methods=['GET'])
@jwt_required()
def get_full_dashboard():
    """
    Return all comprehensive student dashboard data in a single unified response:
    - User information
    - Today's tasks & upcoming tasks
    - Today's schedule
    - Study time & streak
    - Quiz performance
    - Subject progress
    - Recent study sessions
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    # Metrics
    metrics = ProgressService.get_dashboard_metrics(user_id)
    weekly_hours = ProgressService.get_weekly_breakdown(user_id)
    subjects = ProgressService.get_subject_progress(user_id)

    # Tasks
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    today_tasks = [t.to_dict() for t in tasks if not t.completed][:5]
    upcoming_tasks = [t.to_dict() for t in tasks if not t.completed]
    completed_tasks = [t.to_dict() for t in tasks if t.completed]

    # Schedules
    schedules = StudySchedule.query.filter_by(user_id=user_id).order_by(StudySchedule.start_time.asc()).all()

    # Recent study sessions
    recent_sessions = StudySession.query.filter_by(user_id=user_id)\
        .order_by(StudySession.completed_at.desc())\
        .limit(5)\
        .all()

    # Recent completed quizzes
    recent_quizzes = Quiz.query.filter_by(user_id=user_id, completed=True)\
        .order_by(Quiz.created_at.desc())\
        .limit(5)\
        .all()

    return jsonify({
        'success': True,
        'message': 'Dashboard payload generated successfully',
        'data': {
            'user': user.to_dict(),
            'metrics': metrics,
            'weekly_hours': weekly_hours,
            'subjects': subjects,
            'today_tasks': today_tasks,
            'upcoming_tasks': upcoming_tasks,
            'completed_tasks_count': len(completed_tasks),
            'total_tasks_count': len(tasks),
            'schedule': [s.to_dict() for s in schedules],
            'recent_sessions': [s.to_dict() for s in recent_sessions],
            'recent_quizzes': [q.to_dict(include_questions=False) for q in recent_quizzes]
        }
    }), 200
