import { useEffect, useState } from 'react';
import { systemService } from '../services/systemService.js';

export function useSystemStatus() {
  const [state, setState] = useState({
    loading: true,
    online: false,
    status: null,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;
    async function load() {
      const health = await systemService.health();
      const status = await systemService.status();
      if (cancelled) return;
      setState({
        loading: false,
        online: health.success,
        status: status.success ? status.data : null,
        error: health.success ? status.error : health.error,
      });
    }
    load();
    const id = setInterval(load, 30000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  return state;
}
