/* ==========================================================================
   SMARTSTUDY AI - BACKEND REST API CLIENT
   Communicates with Flask REST API at http://localhost:5000 with JWT auth.
   ========================================================================== */

const API_BASE_URL = 'http://localhost:5000/api';

const ApiClient = {
  token: localStorage.getItem('smartstudy_jwt_token') || null,

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('smartstudy_jwt_token', token);
    } else {
      localStorage.removeItem('smartstudy_jwt_token');
    }
  },

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
      const json = await response.json();
      return json;
    } catch (err) {
      console.warn(`[ApiClient] Network request failed for ${endpoint}:`, err);
      return { success: false, message: 'Backend unreachable. Using local storage.', error: err.message };
    }
  },

  // Auth APIs
  async register(name, email, password, university, major) {
    const res = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password, university, major })
    });
    if (res.success && res.data?.token) {
      this.setToken(res.data.token);
    }
    return res;
  },

  async login(email, password) {
    const res = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    if (res.success && res.data?.token) {
      this.setToken(res.data.token);
    }
    return res;
  },

  async getMe() {
    return this.request('/auth/me');
  },

  // Tasks APIs
  async getTasks(status = null, subject = null) {
    let query = '';
    const params = [];
    if (status) params.push(`status=${encodeURIComponent(status)}`);
    if (subject) params.push(`subject=${encodeURIComponent(subject)}`);
    if (params.length) query = '?' + params.join('&');
    return this.request(`/tasks${query}`);
  },

  async createTask(taskData) {
    return this.request('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData)
    });
  },

  async updateTask(taskId, taskData) {
    return this.request(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData)
    });
  },

  async toggleTaskComplete(taskId, completed = null) {
    const body = completed !== null ? JSON.stringify({ completed }) : undefined;
    return this.request(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body
    });
  },

  async deleteTask(taskId) {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE'
    });
  },

  // Study Planner & Schedule APIs
  async getSchedule(date = null) {
    const query = date ? `?date=${encodeURIComponent(date)}` : '';
    return this.request(`/study/schedule${query}`);
  },

  async createScheduleItem(scheduleData) {
    return this.request('/study/schedule', {
      method: 'POST',
      body: JSON.stringify(scheduleData)
    });
  },

  async logStudySession(subject, duration, sessionType = 'pomodoro', notes = '') {
    return this.request('/study/session', {
      method: 'POST',
      body: JSON.stringify({ subject, duration, session_type: sessionType, notes })
    });
  },

  async getStudyStats() {
    return this.request('/study/stats');
  },

  // AI Tutor APIs
  async aiChat(message, subject = 'General', mode = 'socratic') {
    return this.request('/ai/chat', {
      method: 'POST',
      body: JSON.stringify({ message, subject, mode })
    });
  },

  async aiExplain(topic, subject = 'General') {
    return this.request('/ai/explain', {
      method: 'POST',
      body: JSON.stringify({ topic, subject })
    });
  },

  async aiNotes(topic, subject = 'General') {
    return this.request('/ai/notes', {
      method: 'POST',
      body: JSON.stringify({ topic, subject })
    });
  },

  // Quiz APIs
  async generateQuiz(subject, topic = 'General', difficulty = 'medium', numberOfQuestions = 5) {
    return this.request('/quiz/generate', {
      method: 'POST',
      body: JSON.stringify({ subject, topic, difficulty, number_of_questions: numberOfQuestions })
    });
  },

  async submitQuiz(quizId, answers) {
    return this.request(`/quiz/${quizId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  },

  async getQuizHistory() {
    return this.request('/quiz/history');
  },

  // Dashboard & Progress APIs
  async getDashboard() {
    return this.request('/dashboard');
  },

  async getProgressDashboard() {
    return this.request('/progress/dashboard');
  },

  async getWeeklyProgress() {
    return this.request('/progress/weekly');
  },

  async getSubjectProgress() {
    return this.request('/progress/subjects');
  }
};
