from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import StudySchedule, StudySession
from backend.database.database import db

study_bp = Blueprint('study', __name__, url_prefix='/api/study')

# --------------------------------------------------------------------------
# 1. STUDY SCHEDULE / PLANNER ENDPOINTS
# --------------------------------------------------------------------------

@study_bp.route('/schedule', methods=['GET'])
@jwt_required()
def get_schedules():
    """Retrieve planned study schedules for the user."""
    user_id = int(get_jwt_identity())
    date_filter = request.args.get('date')
    
    query = StudySchedule.query.filter_by(user_id=user_id)
    if date_filter:
        query = query.filter_by(date=date_filter)

    schedules = query.order_by(StudySchedule.date.asc(), StudySchedule.start_time.asc()).all()

    return jsonify({
        'success': True,
        'message': f'Retrieved {len(schedules)} schedule blocks',
        'data': {
            'schedule': [s.to_dict() for s in schedules]
        }
    }), 200


@study_bp.route('/schedule', methods=['POST'])
@jwt_required()
def create_schedule():
    """Create a new study schedule item."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    subject = data.get('subject', '').strip()
    topic = data.get('topic', '').strip()
    date = data.get('date', '').strip()
    start_time = data.get('start_time', '').strip()
    end_time = data.get('end_time', '').strip()
    status = data.get('status', 'upcoming').strip().lower()

    if not subject or not topic or not date:
        return jsonify({'success': False, 'message': 'Subject, topic, and date are required'}), 400

    item = StudySchedule(
        user_id=user_id,
        subject=subject,
        topic=topic,
        date=date,
        start_time=start_time or "09:00 AM",
        end_time=end_time or "10:30 AM",
        status=status if status in ['upcoming', 'in-progress', 'completed'] else 'upcoming'
    )
    db.session.add(item)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Study schedule session created successfully',
        'data': {
            'schedule_item': item.to_dict()
        }
    }), 201


@study_bp.route('/schedule/<int:id>', methods=['PUT'])
@jwt_required()
def update_schedule(id: int):
    """Update a study schedule item."""
    user_id = int(get_jwt_identity())
    item = StudySchedule.query.filter_by(id=id, user_id=user_id).first()

    if not item:
        return jsonify({'success': False, 'message': 'Schedule item not found or access denied'}), 404

    data = request.get_json(silent=True) or {}
    if 'subject' in data and data['subject'].strip():
        item.subject = data['subject'].strip()
    if 'topic' in data and data['topic'].strip():
        item.topic = data['topic'].strip()
    if 'date' in data and data['date'].strip():
        item.date = data['date'].strip()
    if 'start_time' in data:
        item.start_time = data['start_time'].strip()
    if 'end_time' in data:
        item.end_time = data['end_time'].strip()
    if 'status' in data and data['status'] in ['upcoming', 'in-progress', 'completed']:
        item.status = data['status']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Schedule updated successfully',
        'data': {
            'schedule_item': item.to_dict()
        }
    }), 200


@study_bp.route('/schedule/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(id: int):
    """Delete a study schedule item."""
    user_id = int(get_jwt_identity())
    item = StudySchedule.query.filter_by(id=id, user_id=user_id).first()

    if not item:
        return jsonify({'success': False, 'message': 'Schedule item not found or access denied'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Schedule item deleted successfully'
    }), 200


# --------------------------------------------------------------------------
# 2. POMODORO / STUDY SESSIONS & STATS ENDPOINTS
# --------------------------------------------------------------------------

@study_bp.route('/session', methods=['POST'])
@jwt_required()
def log_study_session():
    """Log a completed Pomodoro or focus study session."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    subject = data.get('subject', 'General Study').strip()
    duration = int(data.get('duration', 25)) # duration in minutes
    session_type = data.get('session_type', 'pomodoro').strip()
    notes = data.get('notes', '').strip()

    if duration <= 0:
        return jsonify({'success': False, 'message': 'Duration must be greater than 0 minutes'}), 400

    session = StudySession(
        user_id=user_id,
        subject=subject,
        duration=duration,
        session_type=session_type,
        notes=notes,
        completed_at=datetime.utcnow()
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Study session logged successfully',
        'data': {
            'session': session.to_dict()
        }
    }), 201


@study_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_study_sessions():
    """Retrieve logged study session history."""
    user_id = int(get_jwt_identity())
    limit = int(request.args.get('limit', 20))

    sessions = StudySession.query.filter_by(user_id=user_id)\
        .order_by(StudySession.completed_at.desc())\
        .limit(limit)\
        .all()

    return jsonify({
        'success': True,
        'message': f'Retrieved {len(sessions)} study sessions',
        'data': {
            'sessions': [s.to_dict() for s in sessions]
        }
    }), 200


@study_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_study_stats():
    """Calculate today's study time, weekly study time, total study time, and session count."""
    user_id = int(get_jwt_identity())
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=now.weekday())

    all_sessions = StudySession.query.filter_by(user_id=user_id).all()

    # Total study time
    total_minutes = sum(s.duration for s in all_sessions)
    total_sessions_count = len(all_sessions)

    # Today's study time
    today_minutes = sum(s.duration for s in all_sessions if s.completed_at >= today_start)

    # Weekly study time
    weekly_minutes = sum(s.duration for s in all_sessions if s.completed_at >= week_start)

    return jsonify({
        'success': True,
        'message': 'Study statistics calculated successfully',
        'data': {
            'today_minutes': today_minutes,
            'today_formatted': f"{today_minutes // 60}h {today_minutes % 60}m",
            'weekly_minutes': weekly_minutes,
            'weekly_hours': round(weekly_minutes / 60.0, 1),
            'total_minutes': total_minutes,
            'total_hours': round(total_minutes / 60.0, 1),
            'total_sessions': total_sessions_count
        }
    }), 200
