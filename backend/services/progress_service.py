from datetime import datetime, timedelta
from sqlalchemy import func
from backend.models import Task, StudySession, Quiz, User
from backend.database.database import db

class ProgressService:
    """Dynamic progress and analytics calculation service."""

    @staticmethod
    def get_dashboard_metrics(user_id: int) -> dict:
        """Compute live core KPI metrics from SQLite database."""
        user = User.query.get(user_id)
        if not user:
            return {}

        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        week_start = today_start - timedelta(days=now.weekday()) # Monday

        # 1. Today's study minutes
        today_sessions = StudySession.query.filter(
            StudySession.user_id == user_id,
            StudySession.completed_at >= today_start
        ).all()
        today_study_minutes = sum(s.duration for s in today_sessions)

        # 2. Tasks breakdown
        total_tasks = Task.query.filter_by(user_id=user_id).all()
        completed_tasks = sum(1 for t in total_tasks if t.completed)
        pending_tasks = sum(1 for t in total_tasks if not t.completed)

        # 3. Quiz average
        completed_quizzes = Quiz.query.filter_by(user_id=user_id, completed=True).all()
        if completed_quizzes:
            quiz_average = round(sum(q.percentage for q in completed_quizzes) / len(completed_quizzes), 1)
        else:
            quiz_average = 0.0

        # 4. Weekly study hours
        weekly_sessions = StudySession.query.filter(
            StudySession.user_id == user_id,
            StudySession.completed_at >= week_start
        ).all()
        weekly_minutes = sum(s.duration for s in weekly_sessions)
        weekly_study_hours = round(weekly_minutes / 60.0, 1)

        # 5. Study streak (from user profile or calculated)
        study_streak = user.streak or 1

        return {
            "study_streak": study_streak,
            "today_study_minutes": today_study_minutes,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "quiz_average": quiz_average,
            "weekly_study_hours": weekly_study_hours
        }

    @staticmethod
    def get_weekly_breakdown(user_id: int) -> list:
        """Calculate daily study hours for Mon through Sun."""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        monday = today_start - timedelta(days=now.weekday())

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_data = []

        for i in range(7):
            day_start = monday + timedelta(days=i)
            day_end = day_start + timedelta(days=1)

            sessions = StudySession.query.filter(
                StudySession.user_id == user_id,
                StudySession.completed_at >= day_start,
                StudySession.completed_at < day_end
            ).all()

            hours = round(sum(s.duration for s in sessions) / 60.0, 1)
            is_today = (day_start.date() == today_start.date())
            label = f"{hours} hrs" + (" (Today)" if is_today else "")

            weekly_data.append({
                "day": days[i],
                "date": day_start.strftime("%Y-%m-%d"),
                "hours": hours,
                "label": label
            })

        return weekly_data

    @staticmethod
    def get_subject_progress(user_id: int) -> list:
        """Calculate mastery score for each active subject."""
        # Find distinct subjects across tasks and study sessions
        tasks = Task.query.filter_by(user_id=user_id).all()
        quizzes = Quiz.query.filter_by(user_id=user_id, completed=True).all()
        sessions = StudySession.query.filter_by(user_id=user_id).all()

        subjects_set = set(t.subject for t in tasks) | set(q.subject for q in quizzes) | set(s.subject for s in sessions)
        if not subjects_set:
            subjects_set = {"Computer Science", "Mathematics", "Physics", "Chemistry"}

        color_map = {
            "Computer Science": "var(--subject-cs)",
            "Mathematics": "var(--subject-math)",
            "Physics": "var(--subject-physics)",
            "Chemistry": "var(--subject-chem)",
            "Organic Chemistry": "var(--subject-chem)",
            "Biology": "var(--subject-bio)"
        }

        subject_stats = []
        for subj in sorted(subjects_set):
            # Calculate completion metric
            subj_tasks = [t for t in tasks if t.subject == subj]
            task_ratio = (sum(1 for t in subj_tasks if t.completed) / len(subj_tasks)) if subj_tasks else 0.5

            subj_quizzes = [q for q in quizzes if q.subject == subj]
            quiz_ratio = (sum(q.percentage for q in subj_quizzes) / (len(subj_quizzes) * 100)) if subj_quizzes else 0.7

            mastery = round((task_ratio * 0.4 + quiz_ratio * 0.6) * 100)
            mastery = max(10, min(100, mastery)) # clamp between 10% and 100%

            subject_stats.append({
                "subject": subj,
                "percentage": mastery,
                "color": color_map.get(subj, "var(--primary-500)")
            })

        return subject_stats
