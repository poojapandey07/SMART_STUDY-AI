/* ==========================================================================
   SMARTSTUDY AI - COMMAND PALETTE (CTRL+K / CMD+K) CONTROLLER
   ========================================================================== */

const CommandPalette = {
  isOpen: false,

  commands: [
    { title: "Go to Dashboard", category: "Navigation", icon: "📊", action: () => App.navigateTo('dashboard') },
    { title: "Open Study Planner", category: "Navigation", icon: "📅", action: () => App.navigateTo('planner') },
    { title: "Ask AI Tutor", category: "Navigation", icon: "🤖", action: () => App.navigateTo('tutor') },
    { title: "Generate Subject Quiz", category: "Navigation", icon: "🎯", action: () => App.navigateTo('quiz') },
    { title: "Start Pomodoro Focus Timer", category: "Quick Action", icon: "⏱️", action: () => App.navigateTo('pomodoro') },
    { title: "View Progress & Analytics", category: "Navigation", icon: "📈", action: () => App.navigateTo('progress') },
    { title: "Open Settings", category: "Navigation", icon: "⚙️", action: () => App.navigateTo('settings') },
    { title: "Create New Study Task", category: "Quick Action", icon: "➕", action: () => { App.navigateTo('planner'); Planner.openAddTaskModal(); } },
    { title: "Toggle Light / Dark Mode", category: "Settings", icon: "🌓", action: () => {
      const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      Settings.applyTheme(current);
    }},
    { title: "View Landing Page", category: "Navigation", icon: "🚀", action: () => App.navigateTo('landing') }
  ],

  init() {
    this.bindEvents();
    this.renderCommands(this.commands);
  },

  bindEvents() {
    // Keyboard Shortcut (Ctrl+K or Cmd+K)
    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.toggle();
      }
      if (e.key === 'Escape' && this.isOpen) {
        this.close();
      }
    });

    // Topbar Search bar click
    const topbarSearch = document.getElementById('topbar-search-trigger');
    if (topbarSearch) {
      topbarSearch.addEventListener('click', () => this.open());
    }

    // Modal Backdrop Close
    const paletteBackdrop = document.getElementById('command-palette-modal');
    if (paletteBackdrop) {
      paletteBackdrop.addEventListener('click', (e) => {
        if (e.target === paletteBackdrop) this.close();
      });
    }

    // Search Input Filtering
    const searchInput = document.getElementById('palette-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        const filtered = this.commands.filter(cmd => 
          cmd.title.toLowerCase().includes(query) || cmd.category.toLowerCase().includes(query)
        );
        this.renderCommands(filtered);
      });
    }
  },

  toggle() {
    if (this.isOpen) this.close();
    else this.open();
  },

  open() {
    this.isOpen = true;
    const modal = document.getElementById('command-palette-modal');
    const input = document.getElementById('palette-search-input');
    if (modal) {
      modal.classList.add('open');
      if (input) {
        input.value = '';
        this.renderCommands(this.commands);
        setTimeout(() => input.focus(), 50);
      }
    }
  },

  close() {
    this.isOpen = false;
    const modal = document.getElementById('command-palette-modal');
    if (modal) modal.classList.remove('open');
  },

  renderCommands(items) {
    const listEl = document.getElementById('palette-results-list');
    if (!listEl) return;

    if (items.length === 0) {
      listEl.innerHTML = `
        <div style="padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
          No matching commands or pages found.
        </div>
      `;
      return;
    }

    listEl.innerHTML = items.map((cmd, idx) => `
      <div class="palette-item" onclick="CommandPalette.execute(${idx})" style="padding: 0.75rem 1rem; display: flex; align-items: center; gap: 12px; cursor: pointer; border-radius: 8px; transition: background 0.15s ease;">
        <span style="font-size: 1.1rem;">${cmd.icon}</span>
        <div style="flex: 1;">
          <div style="font-size: 0.875rem; font-weight: 600; color: var(--text-primary);">${cmd.title}</div>
          <div style="font-size: 0.7rem; color: var(--text-muted);">${cmd.category}</div>
        </div>
        <span style="font-size: 0.7rem; color: var(--text-muted); background: var(--bg-surface-subtle); padding: 2px 6px; border-radius: 4px;">Jump ↵</span>
      </div>
    `).join('');
  },

  execute(index) {
    const input = document.getElementById('palette-search-input');
    const query = input ? input.value.toLowerCase().trim() : '';
    const filtered = query ? this.commands.filter(cmd => 
      cmd.title.toLowerCase().includes(query) || cmd.category.toLowerCase().includes(query)
    ) : this.commands;

    if (filtered[index]) {
      this.close();
      filtered[index].action();
    }
  }
};
