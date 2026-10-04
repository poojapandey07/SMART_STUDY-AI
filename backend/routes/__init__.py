from .auth_routes import auth_bp
from .task_routes import task_bp
from .study_routes import study_bp
from .ai_routes import ai_bp
from .quiz_routes import quiz_bp
from .progress_routes import progress_bp
from .dashboard_routes import dashboard_bp

__all__ = [
    'auth_bp',
    'task_bp',
    'study_bp',
    'ai_bp',
    'quiz_bp',
    'progress_bp',
    'dashboard_bp'
]
