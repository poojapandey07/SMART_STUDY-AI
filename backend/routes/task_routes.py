from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Task
from backend.database.database import db

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@task_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """Retrieve all study tasks for the authenticated student with optional filtering."""
    user_id = int(get_jwt_identity())
    
    query = Task.query.filter_by(user_id=user_id)
    
    # Filter by completion status
    status_filter = request.args.get('status')
    if status_filter == 'completed':
        query = query.filter_by(completed=True)
    elif status_filter == 'pending':
        query = query.filter_by(completed=False)

    # Filter by subject
    subject_filter = request.args.get('subject')
    if subject_filter:
        query = query.filter(Task.subject.ilike(f'%{subject_filter}%'))

    # Order by creation date descending
    tasks = query.order_by(Task.created_at.desc()).all()

    return jsonify({
        'success': True,
        'message': f'Retrieved {len(tasks)} tasks',
        'data': {
            'tasks': [t.to_dict() for t in tasks]
        }
    }), 200


@task_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new study task."""
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    title = data.get('title', '').strip()
    subject = data.get('subject', '').strip()
    description = data.get('description', '').strip()
    priority = data.get('priority', 'med').strip().lower()
    deadline = data.get('deadline', '').strip()
    duration = data.get('duration', '45 min').strip()

    if not title:
        return jsonify({'success': False, 'message': 'Task title is required'}), 400
    if not subject:
        return jsonify({'success': False, 'message': 'Subject is required'}), 400
    if priority not in ['high', 'med', 'low']:
        priority = 'med'

    task = Task(
        user_id=user_id,
        title=title,
        subject=subject,
        description=description,
        priority=priority,
        deadline=deadline,
        duration=duration,
        completed=False
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Study task created successfully',
        'data': {
            'task': task.to_dict()
        }
    }), 201


@task_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id: int):
    """Update an existing study task."""
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({'success': False, 'message': 'Task not found or access denied'}), 404

    data = request.get_json(silent=True) or {}
    if 'title' in data and data['title'].strip():
        task.title = data['title'].strip()
    if 'subject' in data and data['subject'].strip():
        task.subject = data['subject'].strip()
    if 'description' in data:
        task.description = data['description'].strip()
    if 'priority' in data and data['priority'] in ['high', 'med', 'low']:
        task.priority = data['priority']
    if 'deadline' in data:
        task.deadline = data['deadline'].strip()
    if 'duration' in data:
        task.duration = data['duration'].strip()
    if 'completed' in data:
        task.completed = bool(data['completed'])

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task updated successfully',
        'data': {
            'task': task.to_dict()
        }
    }), 200


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id: int):
    """Delete a study task."""
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({'success': False, 'message': 'Task not found or access denied'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task deleted successfully'
    }), 200


@task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
@jwt_required()
def toggle_task_complete(task_id: int):
    """Toggle or set the completion status of a study task."""
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({'success': False, 'message': 'Task not found or access denied'}), 404

    data = request.get_json(silent=True) or {}
    if 'completed' in data:
        task.completed = bool(data['completed'])
    else:
        task.completed = not task.completed

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Task marked as {'completed' if task.completed else 'pending'}",
        'data': {
            'task': task.to_dict()
        }
    }), 200
