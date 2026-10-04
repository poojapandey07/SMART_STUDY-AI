from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.services.ai_service import AIService

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

@ai_bp.route('/chat', methods=['POST'])
@jwt_required(optional=True)
def ai_chat():
    """Chat with AI Study Assistant."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    subject = data.get('subject', 'General').strip()
    mode = data.get('mode', 'socratic').strip()

    if not message:
        return jsonify({'success': False, 'message': 'Message is required'}), 400

    try:
        response_data = AIService.chat(message, subject, mode)
        return jsonify({
            'success': True,
            'message': 'AI response generated successfully',
            'data': response_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'AI Service error: {str(e)}'
        }), 500


@ai_bp.route('/explain', methods=['POST'])
@jwt_required(optional=True)
def ai_explain():
    """Generate simple explanation with examples and key takeaways."""
    data = request.get_json() or {}
    topic = data.get('topic') or data.get('message', '').strip()
    subject = data.get('subject', 'General').strip()

    if not topic:
        return jsonify({'success': False, 'message': 'Topic is required for explanation'}), 400

    try:
        explanation = AIService.explain(topic, subject)
        return jsonify({
            'success': True,
            'message': 'Topic explanation generated successfully',
            'data': explanation
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'AI Service error: {str(e)}'
        }), 500


@ai_bp.route('/notes', methods=['POST'])
@jwt_required(optional=True)
def ai_notes():
    """Generate high-yield revision notes for an academic topic."""
    data = request.get_json() or {}
    topic = data.get('topic') or data.get('message', '').strip()
    subject = data.get('subject', 'General').strip()

    if not topic:
        return jsonify({'success': False, 'message': 'Topic is required to generate notes'}), 400

    try:
        notes_data = AIService.notes(topic, subject)
        return jsonify({
            'success': True,
            'message': 'Revision notes generated successfully',
            'data': notes_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'AI Service error: {str(e)}'
        }), 500
