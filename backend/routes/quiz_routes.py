from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import Quiz
from backend.services.quiz_service import QuizService

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

@quiz_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_quiz():
    """Generate a custom multiple-choice quiz."""
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    subject = data.get('subject', 'Computer Science').strip()
    topic = data.get('topic', 'General').strip()
    difficulty = data.get('difficulty', 'medium').strip().lower()
    count = int(data.get('number_of_questions', 5))

    if count <= 0 or count > 20:
        count = 5

    try:
        quiz = QuizService.generate_quiz(
            user_id=user_id,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            count=count
        )

        return jsonify({
            'success': True,
            'message': f'Generated quiz with {len(quiz.questions)} questions',
            'data': {
                'quiz': quiz.to_dict(include_questions=True)
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to generate quiz: {str(e)}'
        }), 500


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@jwt_required()
def get_quiz_details(quiz_id: int):
    """Retrieve quiz details and questions."""
    user_id = int(get_jwt_identity())
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user_id).first()

    if not quiz:
        return jsonify({'success': False, 'message': 'Quiz not found or access denied'}), 404

    return jsonify({
        'success': True,
        'message': 'Quiz retrieved successfully',
        'data': {
            'quiz': quiz.to_dict(include_questions=True)
        }
    }), 200


@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id: int):
    """Grade submitted quiz answers, store score, and return performance review."""
    user_id = int(get_jwt_identity())
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user_id).first()

    if not quiz:
        return jsonify({'success': False, 'message': 'Quiz not found or access denied'}), 404

    data = request.get_json() or {}
    answers = data.get('answers', {})

    try:
        results = QuizService.grade_quiz(quiz, answers)
        return jsonify({
            'success': True,
            'message': 'Quiz submitted and graded successfully',
            'data': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Grading error: {str(e)}'
        }), 500


@quiz_bp.route('/history', methods=['GET'])
@jwt_required()
def get_quiz_history():
    """Retrieve user's historical quiz records."""
    user_id = int(get_jwt_identity())
    limit = int(request.args.get('limit', 20))

    quizzes = Quiz.query.filter_by(user_id=user_id, completed=True)\
        .order_by(Quiz.created_at.desc())\
        .limit(limit)\
        .all()

    return jsonify({
        'success': True,
        'message': f'Retrieved {len(quizzes)} completed quiz records',
        'data': {
            'quizzes': [q.to_dict(include_questions=False) for q in quizzes]
        }
    }), 200
