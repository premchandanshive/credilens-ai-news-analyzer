import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { authService } from '../services/authService.js';
import { storage } from '../utils/storage.js';

export const AuthContext = createContext(null);

const defaultPrefs = {
  theme: 'dark',
  maxClaims: 8,
  includeTransformer: true,
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [prefs, setPrefs] = useState(() => storage.getPrefs() || defaultPrefs);

  const refresh = useCallback(async () => {
    if (!storage.getToken()) {
      setUser(null);
      setLoading(false);
      return;
    }
    const result = await authService.me();
    if (result.success) {
      setUser(result.data);
      if (result.data?.preferences) {
        setPrefs({ ...defaultPrefs, ...result.data.preferences });
        storage.setPrefs({ ...defaultPrefs, ...result.data.preferences });
      }
    } else if (result.error?.code === 'UNAUTHORIZED') {
      storage.setToken(null);
      setUser(null);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const login = useCallback(async (credentials) => {
    const result = await authService.login(credentials);
    if (result.success) {
      await refresh();
    }
    return result;
  }, [refresh]);

  const register = useCallback(async (payload) => {
    const result = await authService.register(payload);
    if (result.success) {
      await refresh();
    }
    return result;
  }, [refresh]);

  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);

  const updateProfile = useCallback(async (fields) => {
    if (!storage.getToken()) {
      if (fields.displayName) {
        setUser((prev) => prev ? { ...prev, displayName: fields.displayName } : { displayName: fields.displayName, email: '', id: 'guest', preferences: prefs });
      }
      return { success: true, data: null, error: null };
    }
    const result = await authService.updateMe(fields);
    if (result.success) await refresh();
    return result;
  }, [prefs, refresh]);

  const updatePreferences = useCallback(async (next) => {
    const merged = { ...prefs, ...next };
    setPrefs(merged);
    storage.setPrefs(merged);
    if (storage.getToken()) {
      await authService.updateMe({ preferences: merged, displayName: user?.displayName });
    }
  }, [prefs, user]);

  const value = useMemo(
    () => ({ user, loading, prefs, login, register, logout, refresh, updatePreferences, updateProfile, setUser }),
    [user, loading, prefs, login, register, logout, refresh, updatePreferences, updateProfile],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
