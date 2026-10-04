/* ==========================================================================
   SMARTSTUDY AI - SETTINGS CONTROLLER
   ========================================================================== */

const Settings = {
  init() {
    this.bindEvents();
    this.loadProfile();
  },

  bindEvents() {
    const profileForm = document.getElementById('settings-profile-form');
    if (profileForm) {
      profileForm.onsubmit = (e) => {
        e.preventDefault();
        this.saveProfile();
      };
    }

    const btnLogout = document.getElementById('btn-logout');
    if (btnLogout) {
      btnLogout.onclick = () => {
        if (confirm('Are you sure you want to log out?')) {
          App.logout();
        }
      };
    }
  },

  loadProfile() {
    const data = AppStorage.load();
    const user = data.user || DEFAULT_DATA.user;

    const nameInput = document.getElementById('set-name');
    const uniInput = document.getElementById('set-uni');
    const majorInput = document.getElementById('set-major');
    const goalInput = document.getElementById('set-goal');

    if (nameInput) nameInput.value = user.name || 'Pooja Sharma';
    if (uniInput) uniInput.value = user.university || 'Government Engineering College';
    if (majorInput) majorInput.value = user.major || 'Computer Science & Engineering';
    if (goalInput) goalInput.value = user.studyGoalHours || 3.5;
  },

  saveProfile() {
    const name = document.getElementById('set-name').value.trim();
    const uni = document.getElementById('set-uni').value.trim();
    const major = document.getElementById('set-major').value.trim();
    const goal = parseFloat(document.getElementById('set-goal').value) || 3.5;

    const data = AppStorage.load();
    data.user.name = name;
    data.user.university = uni;
    data.user.major = major;
    data.user.studyGoalHours = goal;
    AppStorage.save(data);

    App.updateUserSnippet(data.user);
    App.showToast('Profile preferences saved', 'success');
  }
};
