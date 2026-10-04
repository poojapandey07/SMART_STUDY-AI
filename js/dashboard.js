/* ==========================================================================
   SMARTSTUDY AI - DASHBOARD CONTROLLER
   ========================================================================== */

const Dashboard = {
  async init() {
    this.renderGreeting();
    await this.loadData();
    this.initQuickActions();
  },

  renderGreeting() {
    const data = AppStorage.load();
    const user = data.user || DEFAULT_DATA.user;
    const hour = new Date().getHours();
    let timeGreeting = "Good afternoon";
    if (hour < 12) timeGreeting = "Good morning";
    else if (hour >= 17) timeGreeting = "Good evening";

    const greetingEl = document.getElementById('dashboard-greeting-title');
    if (greetingEl) {
      const firstName = user.name ? user.name.split(' ')[0] : 'Pooja';
      greetingEl.innerHTML = `${timeGreeting}, ${firstName} 👋`;
    }
  },

  async loadData() {
    // Try to fetch live metrics from backend if available
    const res = await ApiClient.getDashboard();
    if (res && res.success && res.data) {
      this.renderKPIsFromBackend(res.data.metrics);
      this.renderSchedule(res.data.schedule);
      this.renderTasks(res.data.today_tasks, res.data.upcoming_tasks);
    } else {
      // Use local storage / fallback data
      const localData = AppStorage.load();
      this.renderKPIsFromLocal(localData);
      this.renderSchedule(localData.scheduleToday || DEFAULT_DATA.scheduleToday);
      this.renderTasksFromLocal(localData.tasks || DEFAULT_DATA.tasks);
    }
  },

  renderKPIsFromBackend(metrics) {
    if (!metrics) return;
    const studyHours = Math.floor(metrics.today_study_minutes / 60);
    const studyMins = metrics.today_study_minutes % 60;
    
    document.getElementById('kpi-study-time').textContent = `${studyHours}h ${studyMins}m`;
    document.getElementById('kpi-tasks-done').textContent = `${metrics.completed_tasks} completed`;
    document.getElementById('kpi-tasks-pending').textContent = `${metrics.pending_tasks} remaining`;
    document.getElementById('kpi-streak').textContent = `🔥 ${metrics.study_streak}-day streak`;
  },

  renderKPIsFromLocal(localData) {
    const tasks = localData.tasks || DEFAULT_DATA.tasks;
    const completed = tasks.filter(t => t.completed).length;
    const pending = tasks.filter(t => !t.completed).length;
    const user = localData.user || DEFAULT_DATA.user;

    document.getElementById('kpi-study-time').textContent = `1h 45m`;
    document.getElementById('kpi-tasks-done').textContent = `${completed} completed`;
    document.getElementById('kpi-tasks-pending').textContent = `${pending} remaining`;
    document.getElementById('kpi-streak').textContent = `🔥 ${user.streak || 5}-day streak`;
  },

  renderSchedule(scheduleItems) {
    const container = document.getElementById('dashboard-schedule-list');
    if (!container) return;

    if (!scheduleItems || scheduleItems.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="padding: 1.5rem 1rem;">
          <p class="text-sm text-muted">No scheduled study sessions for today.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = scheduleItems.map(item => `
      <div class="plan-item">
        <div class="plan-content">
          <div class="plan-title">${item.topic || item.title}</div>
          <div class="plan-meta">
            <span class="badge-subject" data-subj="${item.subject}">${item.subject}</span>
            <span>•</span>
            <span>${item.start_time ? item.start_time + ' - ' + item.end_time : item.time}</span>
          </div>
        </div>
        <div>
          ${item.status === 'in-progress' ? '<span class="badge badge-success">In Progress</span>' : 
            item.status === 'completed' ? '<span class="badge badge-primary">Done</span>' : 
            '<span class="badge" style="background:var(--bg-subtle); color:var(--text-muted);">Upcoming</span>'}
        </div>
      </div>
    `).join('');
  },

  renderTasks(todayTasks, upcomingTasks) {
    const container = document.getElementById('dashboard-tasks-list');
    if (!container) return;

    const allDisplay = todayTasks || upcomingTasks || [];
    if (allDisplay.length === 0) {
      container.innerHTML = `
        <div class="empty-state" style="padding: 1.5rem 1rem;">
          <p class="text-sm text-muted">✓ All current tasks completed!</p>
        </div>
      `;
      return;
    }

    container.innerHTML = allDisplay.slice(0, 4).map(task => `
      <div class="plan-item ${task.completed ? 'completed' : ''}">
        <label class="custom-checkbox" onclick="Dashboard.toggleTask(${task.id}, event)">
          <input type="checkbox" ${task.completed ? 'checked' : ''}>
          <span class="checkmark"></span>
        </label>
        <div class="plan-content">
          <div class="plan-title">${task.title}</div>
          <div class="plan-meta">
            <span class="badge-subject" data-subj="${task.subject}">${task.subject}</span>
            <span>•</span>
            <span class="priority-pill ${task.priority}">${task.priority ? task.priority.toUpperCase() : 'MED'}</span>
            <span>•</span>
            <span>${task.deadline || 'Today'}</span>
          </div>
        </div>
      </div>
    `).join('');
  },

  renderTasksFromLocal(tasks) {
    const pending = tasks.filter(t => !t.completed);
    this.renderTasks(pending.length ? pending : tasks, null);
  },

  async toggleTask(taskId, event) {
    if (event) event.stopPropagation();

    // Call API
    await ApiClient.toggleTaskComplete(taskId);

    // Sync local storage
    const data = AppStorage.load();
    const task = data.tasks.find(t => t.id == taskId);
    if (task) {
      task.completed = !task.completed;
      AppStorage.save(data);
    }

    SoundFX.playSuccessChime();
    App.showToast('Task updated', 'success');
    this.loadData();
    if (typeof Planner !== 'undefined') Planner.loadTasks();
  },

  initQuickActions() {
    const btnAdd = document.getElementById('qa-add-task');
    const btnAI = document.getElementById('qa-ask-ai');
    const btnTimer = document.getElementById('qa-start-timer');
    const btnQuiz = document.getElementById('qa-take-quiz');

    if (btnAdd) btnAdd.onclick = () => { App.navigateTo('planner'); Planner.openAddModal(); };
    if (btnAI) btnAI.onclick = () => App.navigateTo('tutor');
    if (btnTimer) btnTimer.onclick = () => App.navigateTo('pomodoro');
    if (btnQuiz) btnQuiz.onclick = () => App.navigateTo('quiz');
  }
};
