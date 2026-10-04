/* ==========================================================================
   SMARTSTUDY AI - STUDY PLANNER CONTROLLER
   ========================================================================== */

const Planner = {
  currentFilter: 'all',
  editingTaskId: null,

  init() {
    this.bindEvents();
    this.loadTasks();
  },

  bindEvents() {
    // Filter pills
    const filterPills = document.querySelectorAll('.planner-filter-pill');
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.currentFilter = pill.dataset.filter || 'all';
        this.loadTasks();
      });
    });

    // Add Task Button
    const btnAdd = document.getElementById('btn-planner-add');
    if (btnAdd) btnAdd.onclick = () => this.openAddModal();

    // Task Form Submit
    const form = document.getElementById('task-form');
    if (form) {
      form.onsubmit = (e) => {
        e.preventDefault();
        this.saveTask();
      };
    }

    // Modal Close buttons
    const btnClose = document.getElementById('modal-task-close');
    const btnCancel = document.getElementById('modal-task-cancel');
    if (btnClose) btnClose.onclick = () => this.closeModal();
    if (btnCancel) btnCancel.onclick = () => this.closeModal();
  },

  async loadTasks() {
    const container = document.getElementById('planner-task-list');
    if (!container) return;

    let tasks = [];
    const res = await ApiClient.getTasks();
    if (res && res.success && res.data && res.data.tasks) {
      tasks = res.data.tasks;
    } else {
      const local = AppStorage.load();
      tasks = local.tasks || DEFAULT_DATA.tasks;
    }

    // Apply Filter
    if (this.currentFilter === 'pending') {
      tasks = tasks.filter(t => !t.completed);
    } else if (this.currentFilter === 'completed') {
      tasks = tasks.filter(t => t.completed);
    } else if (this.currentFilter !== 'all') {
      tasks = tasks.filter(t => t.subject === this.currentFilter);
    }

    if (tasks.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📋</div>
          <div class="empty-state-text">
            <strong>No study tasks found</strong><br>
            Add your first task to get started with your study session.
          </div>
          <button class="btn btn-primary btn-sm" onclick="Planner.openAddModal()">+ Add Study Task</button>
        </div>
      `;
      return;
    }

    container.innerHTML = tasks.map(task => `
      <div class="task-row-card ${task.completed ? 'completed' : ''}" id="task-row-${task.id}">
        <label class="custom-checkbox" onclick="Planner.toggleTask(${task.id}, event)">
          <input type="checkbox" ${task.completed ? 'checked' : ''}>
          <span class="checkmark"></span>
        </label>
        
        <div style="flex: 1; min-width: 0;">
          <div class="task-title-text">${this.escapeHtml(task.title)}</div>
          <div class="flex items-center gap-2 text-xs text-muted" style="flex-wrap: wrap;">
            <span class="badge-subject" data-subj="${task.subject}">${task.subject}</span>
            <span class="priority-pill ${task.priority}">${task.priority ? task.priority.toUpperCase() : 'MED'}</span>
            <span>•</span>
            <span>⏱️ ${task.duration || '45 min'}</span>
            <span>•</span>
            <span>📅 ${task.deadline || 'Today'}</span>
          </div>
        </div>

        <div class="flex items-center gap-1">
          <button class="btn-icon btn-sm" onclick="Planner.openEditModal(${task.id})" title="Edit Task">
            ✏️
          </button>
          <button class="btn-icon btn-sm" onclick="Planner.deleteTask(${task.id})" title="Delete Task">
            🗑️
          </button>
        </div>
      </div>
    `).join('');
  },

  async toggleTask(taskId, event) {
    if (event) event.stopPropagation();

    await ApiClient.toggleTaskComplete(taskId);

    const local = AppStorage.load();
    const task = local.tasks.find(t => t.id == taskId);
    if (task) {
      task.completed = !task.completed;
      AppStorage.save(local);
    }

    SoundFX.playSuccessChime();
    App.showToast('Task updated', 'success');
    this.loadTasks();
    if (typeof Dashboard !== 'undefined') Dashboard.loadData();
  },

  async deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this study task?')) {
      return;
    }

    await ApiClient.deleteTask(taskId);

    const local = AppStorage.load();
    local.tasks = local.tasks.filter(t => t.id != taskId);
    AppStorage.save(local);

    App.showToast('Task deleted', 'info');
    this.loadTasks();
    if (typeof Dashboard !== 'undefined') Dashboard.loadData();
  },

  openAddModal() {
    this.editingTaskId = null;
    document.getElementById('modal-task-heading').textContent = 'Add Study Task';
    document.getElementById('task-form').reset();
    document.getElementById('task-modal').classList.add('open');
    setTimeout(() => document.getElementById('task-title-input').focus(), 50);
  },

  async openEditModal(taskId) {
    this.editingTaskId = taskId;
    document.getElementById('modal-task-heading').textContent = 'Edit Study Task';

    let task = null;
    const local = AppStorage.load();
    task = local.tasks.find(t => t.id == taskId);

    if (task) {
      document.getElementById('task-title-input').value = task.title;
      document.getElementById('task-subject-select').value = task.subject;
      document.getElementById('task-priority-select').value = task.priority || 'med';
      document.getElementById('task-duration-input').value = task.duration || '45 min';
      document.getElementById('task-deadline-input').value = task.deadline || 'Today, 5:00 PM';
      document.getElementById('task-desc-input').value = task.description || '';
    }

    document.getElementById('task-modal').classList.add('open');
  },

  closeModal() {
    document.getElementById('task-modal').classList.remove('open');
  },

  async saveTask() {
    const title = document.getElementById('task-title-input').value.trim();
    const subject = document.getElementById('task-subject-select').value;
    const priority = document.getElementById('task-priority-select').value;
    const duration = document.getElementById('task-duration-input').value.trim();
    const deadline = document.getElementById('task-deadline-input').value.trim();
    const description = document.getElementById('task-desc-input').value.trim();

    if (!title) {
      App.showToast('Task title is required', 'warning');
      return;
    }

    const payload = { title, subject, priority, duration, deadline, description };

    if (this.editingTaskId) {
      // Update
      await ApiClient.updateTask(this.editingTaskId, payload);
      const local = AppStorage.load();
      const task = local.tasks.find(t => t.id == this.editingTaskId);
      if (task) Object.assign(task, payload);
      AppStorage.save(local);
      App.showToast('Task updated successfully', 'success');
    } else {
      // Create
      const res = await ApiClient.createTask(payload);
      const newId = (res && res.data && res.data.task && res.data.task.id) ? res.data.task.id : Date.now();
      const local = AppStorage.load();
      local.tasks.unshift({ id: newId, completed: false, ...payload });
      AppStorage.save(local);
      App.showToast('Study task created', 'success');
    }

    this.closeModal();
    this.loadTasks();
    if (typeof Dashboard !== 'undefined') Dashboard.loadData();
  },

  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
};
