/* ==========================================================================
   SMARTSTUDY AI - STORAGE CONTROLLER (LOCAL STORAGE SYNC)
   ========================================================================== */

const STORAGE_KEY = 'smartstudy_ai_app_data_v1';

const AppStorage = {
  load() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (e) {
      console.warn('Could not read from localStorage, using default data', e);
    }
    this.save(DEFAULT_DATA);
    return JSON.parse(JSON.stringify(DEFAULT_DATA));
  },

  save(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.error('Could not save to localStorage', e);
    }
  },

  reset() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      this.save(DEFAULT_DATA);
      return JSON.parse(JSON.stringify(DEFAULT_DATA));
    } catch (e) {
      console.error('Failed to reset storage', e);
      return DEFAULT_DATA;
    }
  }
};
