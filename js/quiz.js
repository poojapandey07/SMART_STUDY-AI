/* ==========================================================================
   SMARTSTUDY AI - QUIZ CONTROLLER
   ========================================================================== */

const QuizEngine = {
  currentQuiz: null,
  currentIndex: 0,
  userAnswers: {}, // { questionId: "selected_string" }
  results: null,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const btnGen = document.getElementById('btn-quiz-generate');
    if (btnGen) btnGen.onclick = () => this.generateQuiz();

    const btnNext = document.getElementById('btn-quiz-next');
    if (btnNext) btnNext.onclick = () => this.nextQuestion();

    const btnRetry = document.getElementById('btn-quiz-retry');
    if (btnRetry) btnRetry.onclick = () => this.resetQuiz();
  },

  async generateQuiz() {
    const subject = document.getElementById('quiz-subject-select').value;
    const topic = document.getElementById('quiz-topic-input').value.trim() || 'General';
    const difficulty = document.getElementById('quiz-diff-select').value;
    const count = parseInt(document.getElementById('quiz-count-select').value) || 5;

    const btnGen = document.getElementById('btn-quiz-generate');
    btnGen.disabled = true;
    btnGen.textContent = 'Generating Quiz...';

    const res = await ApiClient.generateQuiz(subject, topic, difficulty, count);
    btnGen.disabled = false;
    btnGen.textContent = 'Start Quiz';

    if (res && res.success && res.data && res.data.quiz) {
      this.currentQuiz = res.data.quiz;
      this.currentIndex = 0;
      this.userAnswers = {};
      this.results = null;

      document.getElementById('quiz-setup-panel').style.display = 'none';
      document.getElementById('quiz-result-panel').style.display = 'none';
      document.getElementById('quiz-play-panel').style.display = 'block';

      this.renderQuestion();
    } else {
      App.showToast('Could not generate quiz. Please try again.', 'error');
    }
  },

  renderQuestion() {
    const q = this.currentQuiz.questions[this.currentIndex];
    const total = this.currentQuiz.questions.length;

    // Header progress
    document.getElementById('quiz-prog-text').textContent = `Question ${this.currentIndex + 1} of ${total}`;
    document.getElementById('quiz-prog-bar').style.width = `${((this.currentIndex + 1) / total) * 100}%`;

    // Question title
    document.getElementById('quiz-q-title').textContent = q.question;

    // Options list
    const optionsContainer = document.getElementById('quiz-options-container');
    const selectedAns = this.userAnswers[q.id] || null;

    optionsContainer.innerHTML = q.options.map((opt, idx) => `
      <div class="quiz-option-item ${selectedAns === opt ? 'selected' : ''}" onclick="QuizEngine.selectOption(${q.id}, '${this.escapeHtml(opt)}')">
        <span style="width: 20px; height: 20px; border-radius: 50%; border: 1.5px solid var(--text-light); display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700;">
          ${String.fromCharCode(65 + idx)}
        </span>
        <span style="flex: 1;">${this.escapeHtml(opt)}</span>
      </div>
    `).join('');

    // Next / Submit button text
    const btnNext = document.getElementById('btn-quiz-next');
    btnNext.textContent = (this.currentIndex === total - 1) ? 'Submit Quiz' : 'Next Question →';
  },

  selectOption(qId, optionText) {
    this.userAnswers[qId] = optionText;
    this.renderQuestion();
  },

  async nextQuestion() {
    const currentQ = this.currentQuiz.questions[this.currentIndex];
    if (!this.userAnswers[currentQ.id]) {
      App.showToast('Please select an option before proceeding', 'warning');
      return;
    }

    if (this.currentIndex < this.currentQuiz.questions.length - 1) {
      this.currentIndex++;
      this.renderQuestion();
    } else {
      // Submit quiz to backend
      const btnNext = document.getElementById('btn-quiz-next');
      btnNext.disabled = true;
      btnNext.textContent = 'Grading...';

      const res = await ApiClient.submitQuiz(this.currentQuiz.id, this.userAnswers);
      btnNext.disabled = false;

      if (res && res.success && res.data) {
        this.results = res.data;
        this.renderResults();
      } else {
        App.showToast('Error grading quiz. Calculating local score.', 'error');
        this.renderLocalResults();
      }
    }
  },

  renderResults() {
    document.getElementById('quiz-play-panel').style.display = 'none';
    document.getElementById('quiz-result-panel').style.display = 'block';

    const data = this.results;
    document.getElementById('quiz-score-badge').textContent = `${data.score} / ${data.total_questions} (${data.percentage}%)`;

    // Render review items with explanations
    const reviewList = document.getElementById('quiz-review-list');
    reviewList.innerHTML = (data.questions || []).map((q, idx) => {
      const isCorrect = q.is_correct;
      return `
        <div style="border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem; margin-bottom: 0.65rem; background: var(--bg-surface);">
          <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 4px;">
            ${idx + 1}. ${q.question}
          </div>
          <div style="font-size: 0.775rem; margin-bottom: 4px;">
            Your Answer: <strong style="color: ${isCorrect ? 'var(--success-text)' : 'var(--danger-text)'}">${q.user_answer || 'None'}</strong>
            ${isCorrect ? ' ✓' : ` | Correct: <strong style="color: var(--success-text)">${q.correct_answer}</strong>`}
          </div>
          <div style="font-size: 0.725rem; color: var(--text-muted); background: var(--bg-subtle); padding: 4px 8px; border-radius: 4px;">
            💡 ${q.explanation}
          </div>
        </div>
      `;
    }).join('');

    SoundFX.playSuccessChime();
  },

  renderLocalResults() {
    let score = 0;
    const total = this.currentQuiz.questions.length;
    this.currentQuiz.questions.forEach(q => {
      if (this.userAnswers[q.id] === q.correct_answer) score++;
    });
    const percentage = Math.round((score / total) * 100);
    this.results = { score, total_questions: total, percentage, questions: this.currentQuiz.questions };
    this.renderResults();
  },

  resetQuiz() {
    document.getElementById('quiz-result-panel').style.display = 'none';
    document.getElementById('quiz-play-panel').style.display = 'none';
    document.getElementById('quiz-setup-panel').style.display = 'block';
  },

  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
};
