from datetime import datetime
from backend.database.database import db

class Achievement(db.Model):
    """Gamified achievement badge model for students."""
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    badge_key = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), default='')
    icon = db.Column(db.String(20), default='🏆')
    unlocked = db.Column(db.Boolean, default=False)
    progress_text = db.Column(db.String(50), default='0/1')
    unlocked_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        """Serialize Achievement object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'badge_key': self.badge_key,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'unlocked': self.unlocked,
            'progress_text': self.progress_text,
            'unlocked_at': self.unlocked_at.isoformat() if self.unlocked_at else None
        }

    def __repr__(self):
        return f'<Achievement {self.badge_key}: {self.title}>'
