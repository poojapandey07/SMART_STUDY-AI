/* ==========================================================================
   SMARTSTUDY AI - FOCUS TIMER (POMODORO) CONTROLLER
   ========================================================================== */

const PomodoroTimer = {
  modes: {
    study: 25 * 60,
    shortBreak: 5 * 60,
    longBreak: 15 * 60
  },
  currentMode: 'study',
  timeLeft: 25 * 60,
  totalSeconds: 25 * 60,
  timerInterval: null,
  isRunning: false,

  init() {
    this.bindEvents();
    this.updateDisplay();
    this.loadTodaySessions();
  },

  bindEvents() {
    const btnPlay = document.getElementById('btn-timer-start');
    const btnPause = document.getElementById('btn-timer-pause');
    const btnReset = document.getElementById('btn-timer-reset');

    if (btnPlay) btnPlay.onclick = () => this.start();
    if (btnPause) btnPause.onclick = () => this.pause();
    if (btnReset) btnReset.onclick = () => this.reset();

    // Mode tabs
    const modeTabs = document.querySelectorAll('.timer-mode-tab');
    modeTabs.forEach(tab => {
      tab.onclick = () => {
        modeTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.switchMode(tab.dataset.mode);
      };
    });
  },

  switchMode(mode) {
    this.pause();
    this.currentMode = mode;
    this.totalSeconds = this.modes[mode] || (25 * 60);
    this.timeLeft = this.totalSeconds;
    this.updateDisplay();
  },

  start() {
    if (this.isRunning) return;
    this.isRunning = true;

    document.getElementById('btn-timer-start').style.display = 'none';
    document.getElementById('btn-timer-pause').style.display = 'inline-flex';

    this.timerInterval = setInterval(() => {
      this.timeLeft--;
      this.updateDisplay();

      if (this.timeLeft <= 0) {
        this.completeSession();
      }
    }, 1000);
  },

  pause() {
    this.isRunning = false;
    clearInterval(this.timerInterval);

    document.getElementById('btn-timer-start').style.display = 'inline-flex';
    document.getElementById('btn-timer-pause').style.display = 'none';
  },

  reset() {
    this.pause();
    this.timeLeft = this.totalSeconds;
    this.updateDisplay();
  },

  async completeSession() {
    this.pause();
    SoundFX.playTimerComplete();

    const subjectSelect = document.getElementById('timer-subject-select');
    const subject = subjectSelect ? subjectSelect.value : 'Data Structures';
    const durationMinutes = Math.round(this.totalSeconds / 60);

    // Save session to backend
    if (this.currentMode === 'study') {
      await ApiClient.logStudySession(subject, durationMinutes, 'pomodoro', 'Completed 25m focus session');
      App.showToast(`🎉 Focus session logged: +${durationMinutes}m for ${subject}!`, 'success');
      this.switchMode('shortBreak');
    } else {
      App.showToast('Break finished! Ready to resume studying?', 'info');
      this.switchMode('study');
    }

    this.loadTodaySessions();
    if (typeof Dashboard !== 'undefined') Dashboard.loadData();
  },

  updateDisplay() {
    const mins = Math.floor(this.timeLeft / 60);
    const secs = this.timeLeft % 60;
    const timeStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    const displayEl = document.getElementById('timer-display-digits');
    if (displayEl) displayEl.textContent = timeStr;

    document.title = this.isRunning ? `(${timeStr}) SmartStudy AI` : 'SmartStudy AI – Study smarter. Stay consistent.';
  },

  async loadTodaySessions() {
    const listEl = document.getElementById('timer-history-list');
    if (!listEl) return;

    let sessions = [];
    const res = await ApiClient.request('/study/sessions?limit=5');
    if (res && res.success && res.data && res.data.sessions) {
      sessions = res.data.sessions;
    } else {
      sessions = DEFAULT_DATA.recentSessions || [];
    }

    if (sessions.length === 0) {
      listEl.innerHTML = `
        <div class="text-xs text-muted" style="text-align: center; padding: 0.5rem;">
          No sessions recorded yet today. Start your first 25m block!
        </div>
      `;
      return;
    }

    listEl.innerHTML = sessions.map(s => `
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.4rem 0; border-bottom: 1px solid var(--border-subtle); font-size: 0.775rem;">
        <div>
          <span class="badge-subject" data-subj="${s.subject}">${s.subject}</span>
          <span style="color: var(--text-muted); margin-left: 4px;">• ${s.duration} min focus</span>
        </div>
        <span style="color: var(--text-muted); font-size: 0.7rem;">✓ Completed</span>
      </div>
    `).join('');
  }
};
