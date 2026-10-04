import { createContext, useCallback, useMemo, useRef, useState } from 'react';
import { analysisService, subscribeProgress } from '../services/analysisService.js';
import { historyService } from '../services/historyService.js';
import { storage } from '../utils/storage.js';

export const AnalysisContext = createContext(null);

export function AnalysisProvider({ children }) {
  const [current, setCurrent] = useState(null);
  const [status, setStatus] = useState('idle');
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState({ stage: null, completed: [], label: '' });
  const [history, setHistory] = useState({ items: [], total: 0, page: 1, limit: 20 });
  const [historyMeta, setHistoryMeta] = useState({ loading: false, error: null });
  const [notifications, setNotifications] = useState([]);
  const abortRef = useRef(0);

  const pushNotification = useCallback((item) => {
    setNotifications((prev) => [{ id: `${Date.now()}`, read: false, createdAt: new Date().toISOString(), ...item }, ...prev].slice(0, 20));
  }, []);

  const markNotificationsRead = useCallback(() => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  }, []);

  const loadHistory = useCallback(async (params = {}) => {
    setHistoryMeta({ loading: true, error: null });
    const result = await historyService.list(params);
    if (result.success) {
      const data = result.data || {};
      const items = data.items || data.results || (Array.isArray(data) ? data : []);
      setHistory({
        items,
        total: data.total ?? items.length,
        page: data.page ?? 1,
        limit: data.limit ?? 20,
      });
      setHistoryMeta({ loading: false, error: null });
    } else {
      setHistory({ items: [], total: 0, page: 1, limit: 20 });
      setHistoryMeta({ loading: false, error: result.error });
    }
    return result;
  }, []);

  const loadById = useCallback(async (id) => {
    setStatus('loading');
    setError(null);
    setProgress({ stage: null, completed: [], label: '' });
    const result = await analysisService.getById(id);
    if (result.success && result.data) {
      setCurrent(result.data);
      storage.setLastAnalysisId(result.data.id);
      setStatus('success');
    } else {
      setError(result.error);
      setStatus('error');
    }
    return result;
  }, []);

  const runAnalyze = useCallback(async (kind, payload) => {
    const ticket = ++abortRef.current;
    setStatus('analyzing');
    setError(null);
    setProgress({ stage: 'queued', completed: [], label: 'Submitting analysis…' });

    const call =
      kind === 'url'
        ? analysisService.analyzeUrl(payload.url)
        : kind === 'file'
          ? analysisService.analyzeFile(payload.file)
          : analysisService.analyzeText(payload.text, payload.title);

    const started = await call;
    if (ticket !== abortRef.current) return started;

    if (!started.success) {
      setStatus('error');
      setError(started.error);
      setProgress({ stage: 'failed', completed: [], label: '' });
      pushNotification({ title: 'Analysis failed', body: started.error?.message, tone: 'danger' });
      return started;
    }

    const data = started.data;
    const analysisId = data?.id || data?.analysisId;

    if (analysisId && (data?.status === 'queued' || data?.status === 'running' || !data?.credibilityScore)) {
      await subscribeProgress(analysisId, (event) => {
        if (ticket !== abortRef.current) return;
        setProgress((prev) => {
          const completed = [...prev.completed];
          if (event.done && event.stage && !completed.includes(event.stage)) completed.push(event.stage);
          return {
            stage: event.stage,
            label: event.label || prev.label,
            completed,
          };
        });
      });
      const finished = await analysisService.getById(analysisId);
      if (ticket !== abortRef.current) return finished;
      if (finished.success && finished.data) {
        setCurrent(finished.data);
        storage.setLastAnalysisId(finished.data.id);
        setStatus('success');
        pushNotification({ title: 'Analysis complete', body: finished.data.title || 'Credibility assessment ready', tone: 'success' });
        return finished;
      }
      setStatus('error');
      setError(finished.error);
      return finished;
    }

    if (data?.credibilityScore != null || data?.status === 'completed') {
      const normalized = { ...data, id: analysisId || data.id };
      setCurrent(normalized);
      if (normalized.id) storage.setLastAnalysisId(normalized.id);
      setStatus('success');
      setProgress((prev) => ({ ...prev, stage: 'completed', label: 'Complete' }));
      pushNotification({ title: 'Analysis complete', body: normalized.title || 'Credibility assessment ready', tone: 'success' });
      return { success: true, data: normalized, error: null };
    }

    setStatus('error');
    setError({ code: 'INVALID_RESPONSE', message: 'The backend returned an unexpected analysis payload.' });
    return { success: false, data: null, error: { code: 'INVALID_RESPONSE', message: 'Unexpected analysis payload.' } };
  }, [pushNotification]);

  const clearCurrent = useCallback(() => {
    setCurrent(null);
    setStatus('idle');
    setError(null);
    setProgress({ stage: null, completed: [], label: '' });
  }, []);

  const value = useMemo(
    () => ({
      current,
      status,
      error,
      progress,
      history,
      historyMeta,
      notifications,
      runAnalyze,
      loadById,
      loadHistory,
      clearCurrent,
      markNotificationsRead,
      setCurrent,
    }),
    [
      current,
      status,
      error,
      progress,
      history,
      historyMeta,
      notifications,
      runAnalyze,
      loadById,
      loadHistory,
      clearCurrent,
      markNotificationsRead,
    ],
  );

  return <AnalysisContext.Provider value={value}>{children}</AnalysisContext.Provider>;
}
