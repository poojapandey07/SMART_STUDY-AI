# 🎓 SmartStudy AI – Backend API Documentation

A production-style, modular REST API backend for **SmartStudy AI (AI-Powered Student Productivity & Learning Assistant)** built with **Python 3, Flask, SQLAlchemy, SQLite, Flask-JWT-Extended, and Flask-CORS**.

---

## 🏗️ Architecture & Project Structure

```
backend/
│
├── app.py                  # Flask Application Factory & Route Registration
├── config.py               # Environment & App Configuration Class
├── requirements.txt        # Production Dependencies
├── .env.example            # Environment Variables Template
├── .env                    # Local Development Environment (Ignored in Git)
├── seed.py                 # Realistic Demo Data Seeder
├── test_backend.py         # Comprehensive Automated API Test Suite
│
├── database/
│   ├── __init__.py
│   └── database.py         # SQLAlchemy Instance Definition
│
├── models/
│   ├── __init__.py         # Model Exports
│   ├── user.py             # User Model with Password Hashing
│   ├── task.py             # Study Task Model
│   ├── study_session.py    # StudySession & StudySchedule Models
│   ├── quiz.py             # Quiz & QuizQuestion Models
│   └── progress.py         # Achievement Model
│
├── routes/
│   ├── __init__.py         # Blueprint Exports
│   ├── auth_routes.py      # POST /register, POST /login, GET /me
│   ├── task_routes.py      # CRUD Study Tasks & Complete Toggle
│   ├── study_routes.py     # Timetable Schedule & Pomodoro Session Stats
│   ├── ai_routes.py        # POST /chat, POST /explain, POST /notes
│   ├── quiz_routes.py      # POST /generate, GET /:id, POST /submit, GET /history
│   ├── progress_routes.py  # GET /dashboard, GET /weekly, GET /subjects
│   └── dashboard_routes.py # GET /dashboard (Comprehensive Unified Payload)
│
└── services/
    ├── __init__.py         # Service Exports
    ├── ai_service.py       # Gemini / OpenAI Integration & Offline Engine
    ├── quiz_service.py     # Adaptive Question Generator & Grader
    └── progress_service.py # Real-Time Analytics & Streak Calculator
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Create and Activate Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` (already pre-configured for local dev):
```bash
cp .env.example .env
```

Key environment variables in `.env`:
| Variable | Description | Default |
| :--- | :--- | :--- |
| `FLASK_ENV` | Environment mode | `development` |
| `PORT` | Backend server port | `5000` |
| `SECRET_KEY` | Flask session secret | Random Secret |
| `JWT_SECRET_KEY` | JWT signing secret | Random Secret |
| `DATABASE_URL` | SQLite database URI | `sqlite:///smartstudy.db` |
| `AI_API_KEY` | Google Gemini or OpenAI API Key | `""` *(uses smart engine if empty)* |
| `AI_PROVIDER` | AI Provider (`gemini`, `openai`, `mock`) | `mock` |
| `AI_MODEL` | AI Model Name | `gemini-1.5-flash` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |

---

## 🗄️ Database Seeding & Testing

### Seed Demo Student & Data
Populates the SQLite database with realistic student data (*Pooja Sharma*, 5 tasks, 5 schedules, 7 study sessions, completed quizzes, and badges):
```bash
python seed.py
```

**Demo Login Credentials:**
- **Email:** `pooja@smartstudy.ai`
- **Password:** `password123`

### Run Automated API Test Suite
Executes 15 integration test suites across every endpoint:
```bash
python test_backend.py
```

---

## 🖥️ Starting the Flask Server

```bash
python app.py
```
The server will start at **`http://127.0.0.1:5000`** with CORS enabled.

---

## 📚 REST API Endpoint Reference

All endpoints return a consistent JSON schema:
- **Success:** `{"success": true, "message": "...", "data": {...}}`
- **Error:** `{"success": false, "message": "..."}`

### 1. Authentication
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new student account | No |
| `POST` | `/api/auth/login` | Log in and receive JWT token | No |
| `GET` | `/api/auth/me` | Get authenticated user profile | **Yes (JWT)** |

#### Register Request Example:
```json
POST /api/auth/register
{
  "name": "Pooja Sharma",
  "email": "pooja@smartstudy.ai",
  "password": "password123",
  "university": "Stanford University",
  "major": "Computer Science & AI"
}
```

---

### 2. Study Tasks API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/tasks` | Get student tasks (`?status=pending\|completed`) | **Yes** |
| `POST` | `/api/tasks` | Create new study task | **Yes** |
| `PUT` | `/api/tasks/<id>` | Update existing task | **Yes** |
| `DELETE` | `/api/tasks/<id>` | Delete task | **Yes** |
| `PATCH` | `/api/tasks/<id>/complete` | Toggle or set task completion | **Yes** |

#### Create Task Example:
```json
POST /api/tasks
{
  "title": "Complete Binary Search Trees Problem Set",
  "subject": "Computer Science",
  "priority": "high",
  "deadline": "Today, 5:00 PM",
  "duration": "45 min",
  "description": "Implement AVL rotations and node deletion"
}
```

---

### 3. Study Planner & Schedule API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/study/schedule` | Retrieve study schedule blocks | **Yes** |
| `POST` | `/api/study/schedule` | Create new schedule timetable item | **Yes** |
| `PUT` | `/api/study/schedule/<id>` | Update schedule item | **Yes** |
| `DELETE` | `/api/study/schedule/<id>` | Delete schedule item | **Yes** |

---

### 4. Pomodoro & Study Sessions API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/study/session` | Log completed focus session | **Yes** |
| `GET` | `/api/study/sessions` | List recent study sessions | **Yes** |
| `GET` | `/api/study/stats` | Today, weekly, & total study hours | **Yes** |

#### Log Session Example:
```json
POST /api/study/session
{
  "subject": "Organic Chemistry",
  "duration": 25,
  "session_type": "pomodoro",
  "notes": "Reviewed SN1 vs SN2 reaction mechanisms"
}
```

---

### 5. AI Tutor API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/ai/chat` | Conversational tutoring | Optional |
| `POST` | `/api/ai/explain` | Concept simplification & examples | Optional |
| `POST` | `/api/ai/notes` | High-yield revision cheat sheets | Optional |

#### Chat Request Example:
```json
POST /api/ai/chat
{
  "message": "Explain Binary Search Trees simply with an example",
  "subject": "Computer Science",
  "mode": "socratic"
}
```

---

### 6. Quiz Generator API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/quiz/generate` | Generate adaptive multiple-choice quiz | **Yes** |
| `GET` | `/api/quiz/<id>` | Get quiz questions | **Yes** |
| `POST` | `/api/quiz/<id>/submit` | Submit answers & get graded score | **Yes** |
| `GET` | `/api/quiz/history` | List historical quiz scores | **Yes** |

#### Generate Quiz Request Example:
```json
POST /api/quiz/generate
{
  "subject": "Computer Science",
  "topic": "Algorithms",
  "difficulty": "medium",
  "number_of_questions": 5
}
```

---

### 7. Progress & Analytics API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/progress/dashboard` | Live KPI stats (streak, minutes, tasks, quiz avg) | **Yes** |
| `GET` | `/api/progress/weekly` | Mon–Sun daily study hour breakdown | **Yes** |
| `GET` | `/api/progress/subjects` | Subject mastery percentages | **Yes** |

---

### 8. Comprehensive Dashboard API
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/dashboard` | All-in-one unified dashboard payload | **Yes** |

---

## 🌐 Frontend Integration Example

Using vanilla JavaScript `fetch()`:

```javascript
// 1. Authenticate & Save JWT
const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'pooja@smartstudy.ai', password: 'password123' })
});
const { data } = await loginResponse.json();
const token = data.token;

// 2. Fetch Tasks with Bearer Token
const tasksResponse = await fetch('http://localhost:5000/api/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
const tasks = await tasksResponse.json();
console.log(tasks.data.tasks);
```
