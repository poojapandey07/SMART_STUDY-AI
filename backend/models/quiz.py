import json
from datetime import datetime
from backend.database.database import db

class Quiz(db.Model):
    """Quiz assessment model for generated practice questions and test results."""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(200), default='General')
    difficulty = db.Column(db.String(50), default='medium')  # 'beginner', 'medium', 'advanced'
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=5)
    percentage = db.Column(db.Float, default=0.0)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to individual questions
    questions = db.relationship('QuizQuestion', backref='quiz', lazy='select', cascade='all, delete-orphan')

    def to_dict(self, include_questions=True):
        """Serialize Quiz object to dictionary."""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'subject': self.subject,
            'topic': self.topic,
            'difficulty': self.difficulty,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_questions and self.questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        return data

    def __repr__(self):
        return f'<Quiz {self.id}: {self.subject} ({self.score}/{self.total_questions})>'


class QuizQuestion(db.Model):
    """Individual question within a Quiz."""
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False)  # JSON string array of options
    correct_answer = db.Column(db.String(255), nullable=False)
    user_answer = db.Column(db.String(255), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)
    explanation = db.Column(db.Text, default='')

    @property
    def options(self):
        """Parse stored JSON options into list."""
        try:
            return json.loads(self.options_json) if self.options_json else []
        except Exception:
            return []

    @options.setter
    def options(self, value):
        """Serialize list of options into JSON string."""
        self.options_json = json.dumps(value) if isinstance(value, (list, tuple)) else '[]'

    def to_dict(self):
        """Serialize question object to dictionary."""
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question': self.question,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'explanation': self.explanation
        }

    def __repr__(self):
        return f'<QuizQuestion {self.id}: {self.question[:30]}...>'
