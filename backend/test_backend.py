"""
Comprehensive API test suite for SmartStudy AI backend using Flask test client.
"""

import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database.database import db
from backend.seed import seed_database

def run_tests():
    # Re-seed database
    seed_database()
    app = create_app()
    client = app.test_client()

    print("\n" + "="*60)
    print("[TEST] RUNNING COMPREHENSIVE BACKEND API TEST SUITE")
    print("="*60)

    # 1. Health Check
    res = client.get('/api/health')
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("[+] GET /api/health -> 200 OK")

    # 2. Auth: Login with demo student
    res = client.post('/api/auth/login', json={
        'email': 'pooja@smartstudy.ai',
        'password': 'password123'
    })
    assert res.status_code == 200, f"Login failed: {res.data}"
    login_data = json.loads(res.data)
    assert login_data['success'] is True
    token = login_data['data']['token']
    auth_headers = {'Authorization': f'Bearer {token}'}
    print("[+] POST /api/auth/login -> 200 OK (JWT Token received)")

    # 3. Auth: Register new test user
    test_email = 'alex.chen@smartstudy.ai'
    res = client.post('/api/auth/register', json={
        'name': 'Alex Chen',
        'email': test_email,
        'password': 'securepassword',
        'university': 'MIT',
        'major': 'Robotics & AI'
    })
    assert res.status_code == 201, f"Register failed: {res.data}"
    reg_data = json.loads(res.data)
    assert reg_data['success'] is True
    assert reg_data['data']['user']['email'] == test_email
    print("[+] POST /api/auth/register -> 201 Created")

    # 4. Auth: Get Current User (Me)
    res = client.get('/api/auth/me', headers=auth_headers)
    assert res.status_code == 200, f"Auth me failed: {res.data}"
    me_data = json.loads(res.data)
    assert me_data['data']['user']['email'] == 'pooja@smartstudy.ai'
    print("[+] GET /api/auth/me -> 200 OK")

    # 5. Tasks: GET /api/tasks
    res = client.get('/api/tasks', headers=auth_headers)
    assert res.status_code == 200, f"Get tasks failed: {res.data}"
    tasks_data = json.loads(res.data)
    assert len(tasks_data['data']['tasks']) >= 5
    print(f"[+] GET /api/tasks -> 200 OK ({len(tasks_data['data']['tasks'])} tasks)")

    # 6. Tasks: POST /api/tasks
    res = client.post('/api/tasks', headers=auth_headers, json={
        'title': 'Test Algorithm Problem Set',
        'subject': 'Computer Science',
        'priority': 'high',
        'deadline': 'Today, 9:00 PM',
        'duration': '30 min',
        'description': 'Graph traversal and topological sort'
    })
    assert res.status_code == 201, f"Create task failed: {res.data}"
    new_task = json.loads(res.data)['data']['task']
    task_id = new_task['id']
    print(f"[+] POST /api/tasks -> 201 Created (ID: {task_id})")

    # 7. Tasks: PUT /api/tasks/<id>
    res = client.put(f'/api/tasks/{task_id}', headers=auth_headers, json={
        'title': 'Updated Algorithm Problem Set',
        'priority': 'med'
    })
    assert res.status_code == 200
    assert json.loads(res.data)['data']['task']['title'] == 'Updated Algorithm Problem Set'
    print(f"[+] PUT /api/tasks/{task_id} -> 200 OK")

    # 8. Tasks: PATCH /api/tasks/<id>/complete
    res = client.patch(f'/api/tasks/{task_id}/complete', headers=auth_headers)
    assert res.status_code == 200
    assert json.loads(res.data)['data']['task']['completed'] is True
    print(f"[+] PATCH /api/tasks/{task_id}/complete -> 200 OK")

    # 9. Tasks: DELETE /api/tasks/<id>
    res = client.delete(f'/api/tasks/{task_id}', headers=auth_headers)
    assert res.status_code == 200
    print(f"[+] DELETE /api/tasks/{task_id} -> 200 OK")

    # 10. Study: GET & POST /api/study/schedule
    res = client.get('/api/study/schedule', headers=auth_headers)
    assert res.status_code == 200
    scheds = json.loads(res.data)['data']['schedule']
    print(f"[+] GET /api/study/schedule -> 200 OK ({len(scheds)} blocks)")

    res = client.post('/api/study/schedule', headers=auth_headers, json={
        'subject': 'Physics',
        'topic': 'Thermodynamics Problem Session',
        'date': '2026-10-05',
        'start_time': '02:00 PM',
        'end_time': '03:30 PM',
        'status': 'upcoming'
    })
    assert res.status_code == 201
    sched_id = json.loads(res.data)['data']['schedule_item']['id']
    print(f"[+] POST /api/study/schedule -> 201 Created (ID: {sched_id})")

    # 11. Study: Log Session & Stats
    res = client.post('/api/study/session', headers=auth_headers, json={
        'subject': 'Computer Science',
        'duration': 25,
        'session_type': 'pomodoro',
        'notes': 'Deep focus on AVL trees'
    })
    assert res.status_code == 201
    print("[+] POST /api/study/session -> 201 Created (25m session)")

    res = client.get('/api/study/sessions', headers=auth_headers)
    assert res.status_code == 200
    print(f"[+] GET /api/study/sessions -> 200 OK ({len(json.loads(res.data)['data']['sessions'])} sessions)")

    res = client.get('/api/study/stats', headers=auth_headers)
    assert res.status_code == 200
    stats = json.loads(res.data)['data']
    assert stats['today_minutes'] >= 25
    print(f"[+] GET /api/study/stats -> 200 OK (Today: {stats['today_formatted']})")

    # 12. AI Routes
    res = client.post('/api/ai/chat', json={
        'message': 'Explain Binary Search Tree rotations simply',
        'subject': 'Computer Science'
    })
    assert res.status_code == 200
    print("[+] POST /api/ai/chat -> 200 OK")

    res = client.post('/api/ai/explain', json={
        'topic': 'Quantum Superposition',
        'subject': 'Physics'
    })
    assert res.status_code == 200
    print("[+] POST /api/ai/explain -> 200 OK")

    res = client.post('/api/ai/notes', json={
        'topic': 'Cellular Respiration',
        'subject': 'Biology'
    })
    assert res.status_code == 200
    print("[+] POST /api/ai/notes -> 200 OK")

    # 13. Quiz: Generate & Submit
    res = client.post('/api/quiz/generate', headers=auth_headers, json={
        'subject': 'Computer Science',
        'topic': 'Data Structures & BFS',
        'difficulty': 'medium',
        'number_of_questions': 3
    })
    assert res.status_code == 201
    quiz_data = json.loads(res.data)['data']['quiz']
    quiz_id = quiz_data['id']
    questions = quiz_data['questions']
    assert len(questions) == 3
    print(f"[+] POST /api/quiz/generate -> 201 Created (Quiz ID: {quiz_id} with {len(questions)} questions)")

    # Submit answers
    answers_payload = {str(q['id']): q['options'][0] for q in questions}
    res = client.post(f'/api/quiz/{quiz_id}/submit', headers=auth_headers, json={'answers': answers_payload})
    assert res.status_code == 200
    print(f"[+] POST /api/quiz/{quiz_id}/submit -> 200 OK (Score: {json.loads(res.data)['data']['percentage']}%)")

    res = client.get('/api/quiz/history', headers=auth_headers)
    assert res.status_code == 200
    print(f"[+] GET /api/quiz/history -> 200 OK ({len(json.loads(res.data)['data']['quizzes'])} history items)")

    # 14. Progress Routes
    res = client.get('/api/progress/dashboard', headers=auth_headers)
    assert res.status_code == 200
    prog_dash = json.loads(res.data)['data']
    assert 'study_streak' in prog_dash
    assert 'today_study_minutes' in prog_dash
    assert 'completed_tasks' in prog_dash
    assert 'pending_tasks' in prog_dash
    assert 'quiz_average' in prog_dash
    assert 'weekly_study_hours' in prog_dash
    print(f"[+] GET /api/progress/dashboard -> 200 OK: {json.dumps(prog_dash)}")

    res = client.get('/api/progress/weekly', headers=auth_headers)
    assert res.status_code == 200
    print("[+] GET /api/progress/weekly -> 200 OK")

    res = client.get('/api/progress/subjects', headers=auth_headers)
    assert res.status_code == 200
    print("[+] GET /api/progress/subjects -> 200 OK")

    # 15. Comprehensive Dashboard
    res = client.get('/api/dashboard', headers=auth_headers)
    assert res.status_code == 200
    full_dash = json.loads(res.data)['data']
    assert 'user' in full_dash
    assert 'metrics' in full_dash
    assert 'today_tasks' in full_dash
    assert 'schedule' in full_dash
    assert 'recent_sessions' in full_dash
    assert 'subjects' in full_dash
    print("[+] GET /api/dashboard -> 200 OK (All unified data present)")

    print("\n" + "="*60)
    print("[SUCCESS] ALL 15 BACKEND API TEST SUITES PASSED FLAWLESSLY!")
    print("="*60 + "\n")

if __name__ == '__main__':
    run_tests()
