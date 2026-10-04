/* ==========================================================================
   SMARTSTUDY AI - MASTER APP CONTROLLER
   Direct email & password authentication and workspace management.
   ========================================================================== */

const App = {
  currentView: 'auth',
  currentUser: null,

  async init() {
    this.bindGlobalEvents();
    this.initAuthForms();

    // Check if user has an active authenticated session
    const token = localStorage.getItem('smartstudy_jwt_token');
    if (token) {
      const res = await ApiClient.getMe();
      if (res && res.success && res.data && res.data.user) {
        this.currentUser = res.data.user;
        this.updateUserSnippet(this.currentUser);
        this.initModules();
        
        const hash = window.location.hash.replace('#', '');
        if (hash && ['dashboard', 'planner', 'tutor', 'quiz', 'pomodoro', 'progress', 'settings'].includes(hash)) {
          this.navigateTo(hash);
        } else {
          this.navigateTo('dashboard');
        }
        return;
      } else {
        // Token invalid/expired
        ApiClient.setToken(null);
      }
    }

    // Default to direct email Login screen
    this.navigateTo('auth');
  },

  initModules() {
    Dashboard.init();
    Planner.init();
    AITutor.init();
    QuizEngine.init();
    PomodoroTimer.init();
    ProgressTracker.init();
    Settings.init();
  },

  bindGlobalEvents() {
    // Sidebar navigation links
    const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
    navLinks.forEach(link => {
      link.onclick = () => {
        const view = link.dataset.view;
        if (view) this.navigateTo(view);
        this.closeMobileSidebar();
      };
    });

    // Mobile bottom navigation links
    const mobileBtns = document.querySelectorAll('.mobile-nav-btn');
    mobileBtns.forEach(btn => {
      btn.onclick = () => {
        const view = btn.dataset.view;
        if (view) this.navigateTo(view);
      };
    });

    // Mobile menu toggle
    const menuBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('app-sidebar');
    if (menuBtn && sidebar) {
      menuBtn.onclick = () => sidebar.classList.toggle('open');
    }

    // Topbar Quick Add Task button
    const btnTopAdd = document.getElementById('topbar-btn-add');
    if (btnTopAdd) {
      btnTopAdd.onclick = () => {
        this.navigateTo('planner');
        Planner.openAddModal();
      };
    }
  },

  initAuthForms() {
    const tabLogin = document.getElementById('auth-tab-login');
    const tabRegister = document.getElementById('auth-tab-register');
    const nameGroup = document.getElementById('auth-name-group');
    const btnSubmit = document.getElementById('auth-submit-btn');

    if (tabLogin && tabRegister) {
      tabLogin.onclick = () => {
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
        nameGroup.style.display = 'none';
        btnSubmit.textContent = 'Sign In';
      };

      tabRegister.onclick = () => {
        tabRegister.classList.add('active');
        tabLogin.classList.remove('active');
        nameGroup.style.display = 'flex';
        btnSubmit.textContent = 'Create Account';
      };
    }

    const authForm = document.getElementById('auth-form');
    if (authForm) {
      authForm.onsubmit = async (e) => {
        e.preventDefault();
        const isRegister = tabRegister.classList.contains('active');
        const email = document.getElementById('auth-email').value.trim();
        const password = document.getElementById('auth-password').value.trim();
        const name = document.getElementById('auth-name').value.trim();

        if (!email || !password) {
          App.showToast('Please enter both email and password', 'warning');
          return;
        }

        btnSubmit.disabled = true;
        btnSubmit.textContent = isRegister ? 'Creating Account...' : 'Signing In...';

        if (isRegister) {
          if (!name) {
            btnSubmit.disabled = false;
            btnSubmit.textContent = 'Create Account';
            App.showToast('Please enter your full name', 'warning');
            return;
          }

          const res = await ApiClient.register(name, email, password, 'Government Engineering College', 'Computer Science & Engineering');
          btnSubmit.disabled = false;
          btnSubmit.textContent = 'Create Account';

          if (res && res.success) {
            App.showToast('Account created successfully!', 'success');
            this.currentUser = res.data.user;
            this.updateUserSnippet(this.currentUser);
            this.initModules();
            this.navigateTo('dashboard');
          } else {
            App.showToast(res.message || 'Registration failed', 'error');
          }
        } else {
          // Direct Email Login
          const res = await ApiClient.login(email, password);
          btnSubmit.disabled = false;
          btnSubmit.textContent = 'Sign In';

          if (res && res.success) {
            const firstName = res.data.user.name ? res.data.user.name.split(' ')[0] : 'Student';
            App.showToast(`Welcome back, ${firstName}!`, 'success');
            this.currentUser = res.data.user;
            this.updateUserSnippet(this.currentUser);
            this.initModules();
            this.navigateTo('dashboard');
          } else {
            App.showToast(res.message || 'Invalid email or password', 'error');
          }
        }
      };
    }
  },

  navigateTo(viewId) {
    this.currentView = viewId;
    window.location.hash = viewId;

    const authContainer = document.getElementById('view-auth');
    const appShell = document.getElementById('app-shell-layout');
    const pageViews = document.querySelectorAll('.app-page-view');

    if (viewId === 'auth') {
      if (authContainer) authContainer.style.display = 'flex';
      if (appShell) appShell.style.display = 'none';
      return;
    }

    if (authContainer) authContainer.style.display = 'none';
    if (appShell) appShell.style.display = 'flex';

    pageViews.forEach(view => {
      if (view.id === `view-${viewId}`) {
        view.classList.add('active');
      } else {
        view.classList.remove('active');
      }
    });

    // Update sidebar active link
    const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
    navLinks.forEach(l => {
      if (l.dataset.view === viewId) l.classList.add('active');
      else l.classList.remove('active');
    });

    // Update mobile bottom nav
    const mobileBtns = document.querySelectorAll('.mobile-nav-btn');
    mobileBtns.forEach(b => {
      if (b.dataset.view === viewId) b.classList.add('active');
      else b.classList.remove('active');
    });

    // Refresh view specific data
    if (viewId === 'dashboard') Dashboard.loadData();
    if (viewId === 'planner') Planner.loadTasks();
    if (viewId === 'progress') ProgressTracker.loadMetrics();
    if (viewId === 'pomodoro') PomodoroTimer.loadTodaySessions();

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  closeMobileSidebar() {
    const sidebar = document.getElementById('app-sidebar');
    if (sidebar) sidebar.classList.remove('open');
  },

  updateUserSnippet(user) {
    if (!user) return;
    const nameEl = document.getElementById('sidebar-user-name');
    const roleEl = document.getElementById('sidebar-user-role');
    const avatarEl = document.getElementById('sidebar-user-avatar');
    const topbarUserEl = document.getElementById('topbar-user-name');

    if (nameEl) nameEl.textContent = user.name || 'Student';
    if (roleEl) roleEl.textContent = user.major ? user.major.split('&')[0].trim() : 'Computer Science';
    if (avatarEl) avatarEl.textContent = user.name ? user.name.charAt(0).toUpperCase() : 'S';
    if (topbarUserEl) topbarUserEl.textContent = user.name || 'Student';
  },

  logout() {
    ApiClient.setToken(null);
    this.currentUser = null;
    this.showToast('Logged out successfully', 'info');
    this.navigateTo('auth');
  },

  showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 2800);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
