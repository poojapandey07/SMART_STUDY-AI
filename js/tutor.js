/* ==========================================================================
   SMARTSTUDY AI - AI TUTOR CONTROLLER
   ========================================================================== */

const AITutor = {
  isSending: false,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const sendBtn = document.getElementById('btn-tutor-send');
    const input = document.getElementById('tutor-input');
    const promptBtns = document.querySelectorAll('.prompt-btn');

    if (sendBtn && input) {
      sendBtn.onclick = () => this.sendMessage();
      input.onkeydown = (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.sendMessage();
        }
      };
    }

    promptBtns.forEach(btn => {
      btn.onclick = () => {
        const promptText = btn.dataset.prompt || btn.innerText.trim();
        this.sendPrompt(promptText);
      };
    });
  },

  sendPrompt(text) {
    const input = document.getElementById('tutor-input');
    if (input) {
      input.value = text;
      this.sendMessage();
    }
  },

  async sendMessage() {
    if (this.isSending) return;
    const input = document.getElementById('tutor-input');
    const text = input.value.trim();
    if (!text) return;

    const subjectSelect = document.getElementById('tutor-subject-select');
    const subject = subjectSelect ? subjectSelect.value : 'Data Structures';

    // Append User Message
    this.appendMessage('user', text);
    input.value = '';
    this.isSending = true;

    // Show Loading state
    this.showLoading();

    try {
      const res = await ApiClient.aiChat(text, subject);
      this.removeLoading();

      if (res && res.data && res.data.message) {
        this.appendMessage('ai', res.data.message);
      } else {
        this.appendMessage('ai', "I'm having trouble connecting right now, but remember: break down the topic into basic axioms and trace an example step-by-step!");
      }
    } catch (err) {
      this.removeLoading();
      this.appendMessage('ai', "Sorry, I ran into an error generating that response. Please try again.");
    } finally {
      this.isSending = false;
    }
  },

  appendMessage(sender, text) {
    const container = document.getElementById('tutor-chat-messages');
    if (!container) return;

    const row = document.createElement('div');
    row.className = `chat-bubble-row ${sender}`;

    if (sender === 'user') {
      row.innerHTML = `
        <div class="bubble-avatar">P</div>
        <div class="bubble-content">${this.escapeHtml(text)}</div>
      `;
    } else {
      // Format markdown-like bold and bullet points simply
      const formatted = this.formatAIResponse(text);
      row.innerHTML = `
        <div class="bubble-avatar">🤖</div>
        <div class="bubble-content">
          ${formatted}
          <div style="text-align: right; margin-top: 6px;">
            <button class="btn btn-ghost btn-sm" onclick="AITutor.copyNote(this)" style="font-size: 0.7rem; padding: 2px 6px;">
              📋 Copy
            </button>
          </div>
        </div>
      `;
    }

    container.appendChild(row);
    container.scrollTop = container.scrollHeight;
  },

  showLoading() {
    const container = document.getElementById('tutor-chat-messages');
    if (!container) return;

    const loader = document.createElement('div');
    loader.id = 'tutor-loading-bubble';
    loader.className = 'chat-bubble-row ai';
    loader.innerHTML = `
      <div class="bubble-avatar">🤖</div>
      <div class="bubble-content" style="color: var(--text-muted); font-size: 0.8rem;">
        Thinking...
      </div>
    `;
    container.appendChild(loader);
    container.scrollTop = container.scrollHeight;
  },

  removeLoading() {
    const el = document.getElementById('tutor-loading-bubble');
    if (el) el.remove();
  },

  copyNote(btn) {
    const bubble = btn.closest('.bubble-content');
    const text = bubble.innerText.replace('📋 Copy', '').trim();
    navigator.clipboard.writeText(text).then(() => {
      App.showToast('Copied to clipboard', 'success');
    });
  },

  formatAIResponse(text) {
    // Basic clean HTML formatting for markdown-style bold, lists, and code
    let html = this.escapeHtml(text);
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`([^`]+)`/g, '<code style="background:var(--bg-subtle); padding:2px 4px; border-radius:3px; font-family:var(--font-mono);">$1</code>');
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n• /g, '<br>• ');
    return html;
  },

  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
};
