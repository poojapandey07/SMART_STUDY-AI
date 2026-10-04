"""
SmartStudy AI - Database Seed Script
Populates SQLite database with realistic college student data for a student hackathon demo.
"""

import sys
import os
from datetime import datetime, timedelta, timezone

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database.database import db
from backend.models import User, Task, StudySchedule, StudySession, Quiz, QuizQuestion, Achievement

def seed_database():
    app = create_app()
    with app.app_context():
        print("[*] Seeding SmartStudy AI Database with realistic student data...")

        # Drop and recreate tables for a clean slate
        db.drop_all()
        db.create_all()

        # 1. Create Demo Student (Pooja Sharma)
        demo_user = User(
            name="Pooja Sharma",
            email="pooja@smartstudy.ai",
            university="Government Engineering College",
            major="Computer Science & Engineering",
            study_goal_hours=3.5,
            streak=5
        )
        demo_user.set_password("password123")
        db.session.add(demo_user)
        db.session.flush()
        print(f"[+] Created Student: {demo_user.name} ({demo_user.email}) [ID: {demo_user.id}]")

        # 2. Seed Realistic College Study Tasks
        tasks_data = [
            {
                "title": "Revise array operations and two-pointer technique",
                "subject": "Data Structures",
                "description": "Practice two-sum and sliding window problems",
                "priority": "high",
                "deadline": "Today, 5:00 PM",
                "duration": "45 min",
                "completed": True
            },
            {
                "title": "Practice 10 Python list comprehension questions",
                "subject": "Python",
                "description": "Solve dictionary and list comprehension exercises",
                "priority": "high",
                "deadline": "Today, 7:30 PM",
                "duration": "60 min",
                "completed": False
            },
            {
                "title": "Read DBMS normalization notes (1NF to 3NF)",
                "subject": "Database Management",
                "description": "Review functional dependencies and lossless join decomposition",
                "priority": "med",
                "deadline": "Tomorrow, 2:00 PM",
                "duration": "50 min",
                "completed": False
            },
            {
                "title": "Prepare OS process scheduling (Round Robin & SJF)",
                "subject": "Operating Systems",
                "description": "Calculate average waiting time and turnaround time numericals",
                "priority": "med",
                "deadline": "Oct 6, 11:00 AM",
                "duration": "60 min",
                "completed": False
            },
            {
                "title": "Review neural network backpropagation steps",
                "subject": "Artificial Intelligence",
                "description": "Derive chain rule gradients for weights and biases",
                "priority": "low",
                "deadline": "Oct 7, 4:00 PM",
                "duration": "40 min",
                "completed": True
            }
        ]

        for t in tasks_data:
            task = Task(user_id=demo_user.id, **t)
            db.session.add(task)
        print(f"[+] Seeded {len(tasks_data)} Study Tasks")

        # 3. Seed Study Schedule for Today
        schedules_data = [
            {"subject": "Data Structures", "topic": "Array Operations & Two-Pointer Workshop", "date": "2026-10-04", "start_time": "09:00 AM", "end_time": "10:00 AM", "status": "completed"},
            {"subject": "Python", "topic": "List Comprehensions & Generator Functions", "date": "2026-10-04", "start_time": "11:00 AM", "end_time": "12:00 PM", "status": "completed"},
            {"subject": "Database Management", "topic": "Normalization & BCNF Practice", "date": "2026-10-04", "start_time": "02:00 PM", "end_time": "03:15 PM", "status": "in-progress"},
            {"subject": "Operating Systems", "topic": "CPU Scheduling Algorithms & Gantt Charts", "date": "2026-10-04", "start_time": "04:30 PM", "end_time": "05:30 PM", "status": "upcoming"},
            {"subject": "Artificial Intelligence", "topic": "AI Tutor Quick Revision & 5-Question Quiz", "date": "2026-10-04", "start_time": "07:00 PM", "end_time": "07:45 PM", "status": "upcoming"}
        ]

        for s in schedules_data:
            sched = StudySchedule(user_id=demo_user.id, **s)
            db.session.add(sched)
        print(f"[+] Seeded {len(schedules_data)} Study Schedule Items")

        # 4. Seed Realistic Study Sessions (105 mins logged today, ~9.5h this week)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        sessions_data = [
            {"subject": "Data Structures", "duration": 45, "session_type": "pomodoro", "completed_at": now - timedelta(hours=5)},
            {"subject": "Python", "duration": 60, "session_type": "pomodoro", "completed_at": now - timedelta(hours=2)},
            {"subject": "Database Management", "duration": 50, "session_type": "pomodoro", "completed_at": now - timedelta(days=1, hours=4)},
            {"subject": "Operating Systems", "duration": 75, "session_type": "custom", "completed_at": now - timedelta(days=2, hours=3)},
            {"subject": "Data Structures", "duration": 90, "session_type": "custom", "completed_at": now - timedelta(days=3, hours=4)},
            {"subject": "Artificial Intelligence", "duration": 45, "session_type": "pomodoro", "completed_at": now - timedelta(days=4, hours=2)},
            {"subject": "Python", "duration": 60, "session_type": "pomodoro", "completed_at": now - timedelta(days=5, hours=3)}
        ]

        for sess in sessions_data:
            study_sess = StudySession(
                user_id=demo_user.id,
                subject=sess["subject"],
                duration=sess["duration"],
                session_type=sess["session_type"],
                completed_at=sess["completed_at"]
            )
            db.session.add(study_sess)
        print(f"[+] Seeded {len(sessions_data)} Study Sessions")

        # 5. Seed Quizzes
        q1 = Quiz(
            user_id=demo_user.id,
            subject="Data Structures",
            topic="Arrays & Stacks",
            difficulty="medium",
            score=4,
            total_questions=5,
            percentage=80.0,
            completed=True,
            created_at=now - timedelta(days=1)
        )
        db.session.add(q1)
        db.session.flush()

        q1_questions = [
            ("What is the time complexity to access an element by index in an array?", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "O(1)", "O(1)", True, "Arrays support constant time random access via index arithmetic."),
            ("Which data structure operates on a FIFO principle?", ["Stack", "Queue", "Binary Tree", "Max-Heap"], "Queue", "Queue", True, "Queue is First-In First-Out."),
            ("Average time complexity of searching in a Balanced BST?", ["O(1)", "O(log n)", "O(n)", "O(n^2)"], "O(log n)", "O(log n)", True, "Logarithmic height yields O(log n) lookups."),
            ("Which structure is best for undo functionality?", ["Queue", "Stack", "Array", "Hash Table"], "Stack", "Stack", True, "Stack is LIFO so last action is undone first."),
            ("Worst case of standard QuickSort?", ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"], "O(n^2)", "O(n log n)", False, "Unbalanced partitions lead to O(n^2).")
        ]

        for q_text, opts, correct, user_ans, is_corr, exp in q1_questions:
            qq = QuizQuestion(
                quiz_id=q1.id,
                question=q_text,
                options=opts,
                correct_answer=correct,
                user_answer=user_ans,
                is_correct=is_corr,
                explanation=exp
            )
            db.session.add(qq)

        print("[+] Seeded Sample Quiz with 5 Questions")

        # 6. Seed Achievements
        achievements_data = [
            {"badge_key": "streak_5", "title": "5-Day Streak", "description": "Studied 5 consecutive days", "icon": "🔥", "unlocked": True, "progress_text": "5/5 Days"},
            {"badge_key": "quiz_passed", "title": "Quiz Master", "description": "Scored 80%+ on Data Structures quiz", "icon": "🎯", "unlocked": True, "progress_text": "Completed"},
            {"badge_key": "deep_focus", "title": "Focus Session", "description": "Completed 5 Pomodoro sessions this week", "icon": "⏱️", "unlocked": True, "progress_text": "7 Sessions"},
            {"badge_key": "consistent", "title": "Weekly Consistency", "description": "Logged 8+ hours in a single week", "icon": "📈", "unlocked": True, "progress_text": "8.5 hrs"}
        ]

        for ach in achievements_data:
            achievement = Achievement(user_id=demo_user.id, **ach)
            db.session.add(achievement)
        print(f"[+] Seeded {len(achievements_data)} Badges")

        db.session.commit()
        print("\n[SUCCESS] Database successfully seeded with demo student credentials:")
        print("   Email:    pooja@smartstudy.ai")
        print("   Password: password123")

if __name__ == '__main__':
    seed_database()
