from datetime import datetime
from backend.database.database import db

class StudySession(db.Model):
    """Pomodoro and focus study session record model."""
    __tablename__ = 'study_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    session_type = db.Column(db.String(50), default='pomodoro')  # 'pomodoro', 'short_break', 'long_break', 'custom'
    notes = db.Column(db.Text, default='')
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Serialize StudySession object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject': self.subject,
            'duration': self.duration,
            'session_type': self.session_type,
            'notes': self.notes,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<StudySession {self.id}: {self.subject} ({self.duration}m)>'


class StudySchedule(db.Model):
    """Planned daily and weekly study timetable schedule item."""
    __tablename__ = 'study_schedules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # e.g., '2026-10-04'
    start_time = db.Column(db.String(20), nullable=False)  # e.g., '09:00 AM'
    end_time = db.Column(db.String(20), nullable=False)    # e.g., '10:30 AM'
    status = db.Column(db.String(30), default='upcoming')  # 'upcoming', 'in-progress', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Serialize StudySchedule object to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject': self.subject,
            'topic': self.topic,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<StudySchedule {self.id}: {self.subject} - {self.topic}>'
