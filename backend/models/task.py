from datetime import datetime
from backend.database.database import db

class Task(db.Model):
    """Study task model for planning and progress tracking."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    priority = db.Column(db.String(20), default='med')  # 'high', 'med', 'low'
    deadline = db.Column(db.String(100), default='')
    duration = db.Column(db.String(50), default='45 min')
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Serialize Task object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority,
            'deadline': self.deadline,
            'duration': self.duration,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
