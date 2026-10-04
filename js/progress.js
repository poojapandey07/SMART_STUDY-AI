/* ==========================================================================
   SMARTSTUDY AI - PROGRESS & ANALYTICS CONTROLLER
   ========================================================================== */

const ProgressTracker = {
  async init() {
    await this.loadMetrics();
  },

  async loadMetrics() {
    // 1. Dashboard summary numbers
    const resDash = await ApiClient.getProgressDashboard();
    if (resDash && resDash.success && resDash.data) {
      const m = resDash.data;
      document.getElementById('prog-streak-val').textContent = `${m.study_streak} days`;
      document.getElementById('prog-weekly-val').textContent = `${m.weekly_study_hours} hrs`;
      document.getElementById('prog-tasks-val').textContent = `${m.completed_tasks} completed`;
      document.getElementById('prog-quiz-val').textContent = `${m.quiz_average}%`;
    }

    // 2. Weekly Bar Chart
    const resWeekly = await ApiClient.getWeeklyProgress();
    let weekly = DEFAULT_DATA.weeklyHours;
    if (resWeekly && resWeekly.success && resWeekly.data && resWeekly.data.weekly_hours) {
      weekly = resWeekly.data.weekly_hours;
    }
    this.renderBarChart(weekly);

    // 3. Subject-wise Progress
    const resSubj = await ApiClient.getSubjectProgress();
    let subjects = DEFAULT_DATA.subjectProgress;
    if (resSubj && resSubj.success && resSubj.data && resSubj.data.subjects) {
      subjects = resSubj.data.subjects;
    }
    this.renderSubjectMastery(subjects);
  },

  renderBarChart(weekly) {
    const container = document.getElementById('weekly-bar-chart-container');
    if (!container) return;

    const maxHours = Math.max(...weekly.map(d => d.hours), 5);

    container.innerHTML = weekly.map(item => {
      const pct = Math.round((item.hours / maxHours) * 100);
      return `
        <div class="chart-bar-col">
          <div style="font-size: 0.675rem; color: var(--text-muted); font-weight: 600;">${item.hours}h</div>
          <div class="chart-bar-rect" style="height: ${Math.max(pct, 6)}%;"></div>
          <span class="chart-bar-day">${item.day}</span>
        </div>
      `;
    }).join('');
  },

  renderSubjectMastery(subjects) {
    const container = document.getElementById('subject-progress-container');
    if (!container) return;

    container.innerHTML = subjects.map(s => `
      <div style="margin-bottom: 0.85rem;">
        <div class="flex justify-between items-center text-xs font-semibold" style="margin-bottom: 4px;">
          <span>${s.subject}</span>
          <span style="color: var(--primary-600);">${s.percentage}%</span>
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width: ${s.percentage}%;"></div>
        </div>
      </div>
    `).join('');
  }
};
