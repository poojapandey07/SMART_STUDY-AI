from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.database import db

class User(db.Model):
    """User account model with secure password hashing and relationships."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(150), default='Stanford University')
    major = db.Column(db.String(150), default='Computer Science & AI')
    study_goal_hours = db.Column(db.Float, default=5.0)
    streak = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    tasks = db.relationship('Task', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    study_sessions = db.relationship('StudySession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    study_schedules = db.relationship('StudySchedule', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash and securely store password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify given plain-text password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize User object to dictionary without exposing sensitive fields."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'university': self.university,
            'major': self.major,
            'study_goal_hours': self.study_goal_hours,
            'streak': self.streak,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.email}>'
