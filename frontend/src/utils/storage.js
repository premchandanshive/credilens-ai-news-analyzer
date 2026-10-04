const TOKEN_KEY = 'credilens.token';
const THEME_KEY = 'credilens.theme';
const PREFS_KEY = 'credilens.prefs';
const LAST_ANALYSIS_KEY = 'credilens.lastAnalysisId';

export const storage = {
  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },
  setToken(token) {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  },
  getTheme() {
    return localStorage.getItem(THEME_KEY) || 'dark';
  },
  setTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
  },
  getPrefs() {
    try {
      return JSON.parse(localStorage.getItem(PREFS_KEY) || 'null');
    } catch {
      return null;
    }
  },
  setPrefs(prefs) {
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs));
  },
  getLastAnalysisId() {
    return localStorage.getItem(LAST_ANALYSIS_KEY);
  },
  setLastAnalysisId(id) {
    if (id) localStorage.setItem(LAST_ANALYSIS_KEY, id);
    else localStorage.removeItem(LAST_ANALYSIS_KEY);
  },
};
