/* ==========================================================================
   SMARTSTUDY AI - LANDING PAGE INTERACTIONS
   ========================================================================== */

const LandingPage = {
  init() {
    this.bindEvents();
  },

  bindEvents() {
    // CTA Button "Start Studying"
    const btnStart = document.getElementById('btn-landing-start');
    if (btnStart) {
      btnStart.addEventListener('click', () => {
        App.navigateTo('dashboard');
        SoundFX.playSuccessChime();
      });
    }

    // Secondary CTA
    const btnExplore = document.getElementById('btn-landing-explore');
    if (btnExplore) {
      btnExplore.addEventListener('click', () => {
        const featuresEl = document.getElementById('features-section');
        if (featuresEl) featuresEl.scrollIntoView({ behavior: 'smooth' });
      });
    }

    // Bottom CTA
    const btnBottomCta = document.getElementById('btn-landing-bottom-cta');
    if (btnBottomCta) {
      btnBottomCta.addEventListener('click', () => {
        App.navigateTo('dashboard');
        SoundFX.playSuccessChime();
      });
    }

    // Demo Showcase Tab buttons
    const demoTabs = document.querySelectorAll('.demo-tab-btn');
    demoTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        demoTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const view = tab.dataset.view;
        this.switchPreviewContent(view);
      });
    });
  },

  switchPreviewContent(view) {
    const previewContainer = document.getElementById('hero-mock-dynamic-view');
    if (!previewContainer) return;

    if (view === 'tutor') {
      previewContainer.innerHTML = `
        <div style="background:var(--bg-surface); padding:1rem; border-radius:12px; border:1px solid var(--border-color);">
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.8rem; font-weight:700; color:var(--primary-600);">AI Tutor Session</span>
            <span class="badge badge-success" style="font-size:0.65rem;">Active</span>
          </div>
          <div style="background:var(--primary-50); padding:0.65rem; border-radius:8px; font-size:0.75rem; color:var(--primary-900); margin-bottom:6px;">
            <strong>User:</strong> Explain Dijkstra's Algorithm simply with an example.
          </div>
          <div style="background:var(--bg-surface-subtle); padding:0.65rem; border-radius:8px; font-size:0.75rem; line-height:1.4;">
            <strong>AI Tutor:</strong> Dijkstra is like choosing the cheapest direct highway step-by-step until you reach your destination city with guaranteed lowest toll cost!
          </div>
        </div>
      `;
    } else if (view === 'quiz') {
      previewContainer.innerHTML = `
        <div style="background:var(--bg-surface); padding:1rem; border-radius:12px; border:1px solid var(--border-color);">
          <div style="font-size:0.75rem; font-weight:700; color:var(--text-muted); margin-bottom:4px;">Question 3 of 5 • Computer Science</div>
          <div style="font-size:0.85rem; font-weight:800; margin-bottom:8px;">What is the time complexity of QuickSort in the average case?</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.75rem;">
            <div style="padding:6px 8px; border-radius:6px; background:#dcfce7; border:1px solid #86efac; color:#166534; font-weight:700;">✓ O(n log n)</div>
            <div style="padding:6px 8px; border-radius:6px; background:var(--bg-surface-subtle); border:1px solid var(--border-color);">O(n²)</div>
          </div>
        </div>
      `;
    } else if (view === 'pomodoro') {
      previewContainer.innerHTML = `
        <div style="background:var(--bg-surface); padding:1rem; border-radius:12px; border:1px solid var(--border-color); text-align:center;">
          <div style="font-size:0.75rem; font-weight:700; color:var(--primary-600); margin-bottom:4px;">Deep Focus Interval</div>
          <div style="font-size:2rem; font-weight:800; font-family:var(--font-mono); color:var(--text-primary);">24:38</div>
          <div class="badge badge-purple" style="font-size:0.65rem; margin-top:4px;">Organic Chemistry Lab</div>
        </div>
      `;
    } else {
      previewContainer.innerHTML = `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
          <div style="background:var(--bg-surface); padding:0.75rem; border-radius:8px; border:1px solid var(--border-color);">
            <div style="font-size:0.7rem; color:var(--text-muted);">Today's Progress</div>
            <div style="font-size:1.25rem; font-weight:800; color:var(--primary-600);">78%</div>
          </div>
          <div style="background:var(--bg-surface); padding:0.75rem; border-radius:8px; border:1px solid var(--border-color);">
            <div style="font-size:0.7rem; color:var(--text-muted);">Study Streak</div>
            <div style="font-size:1.25rem; font-weight:800; color:#ea580c;">🔥 12 Days</div>
          </div>
        </div>
      `;
    }
  }
};
