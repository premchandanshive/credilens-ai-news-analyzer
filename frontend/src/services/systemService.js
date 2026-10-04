import { request } from './apiClient.js';

export const systemService = {
  async health() {
    return request('get', '/api/health', { timeout: 8000 });
  },
  async status() {
    return request('get', '/api/system/status', { timeout: 8000 });
  },
};
