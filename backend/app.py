import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.config import Config
from backend.database.database import db
from backend.routes import (
    auth_bp,
    task_bp,
    study_bp,
    ai_bp,
    quiz_bp,
    progress_bp,
    dashboard_bp
)

def create_app(config_class=Config):
    """Application factory for SmartStudy AI Flask backend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    jwt = JWTManager(app)

    # JWT Error Handlers for consistent JSON responses
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({
            'success': False,
            'message': 'Authorization token is missing or invalid'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Authorization token has expired. Please log in again.'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({
            'success': False,
            'message': 'Signature verification failed. Invalid token.'
        }), 401

    # Register Route Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(dashboard_bp)

    # Health Check API
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'success': True,
            'message': 'SmartStudy AI Backend is healthy and running',
            'data': {
                'status': 'online',
                'environment': app.config.get('ENV', 'development'),
                'database': 'SQLite'
            }
        }), 200

    # Global HTTP Error Handlers
    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({'success': False, 'message': 'Bad Request: ' + str(e)}), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({'success': False, 'message': 'The requested endpoint was not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed_error(e):
        return jsonify({'success': False, 'message': 'HTTP method not allowed for this endpoint'}), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'success': False, 'message': 'Internal Server Error. Please try again later.'}), 500

    # Auto-create database tables on startup
    with app.app_context():
        db.create_all()

    return app


# Create master app instance
app = create_app()

if __name__ == '__main__':
    port = Config.PORT
    debug = Config.DEBUG
    print(f"🚀 SmartStudy AI Backend running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
