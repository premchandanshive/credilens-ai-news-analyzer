import { request } from './apiClient.js';

export const historyService = {
  async list({ q = '', sort = 'createdAt_desc', page = 1, limit = 20, from, to } = {}) {
    return request('get', '/api/analysis/history', {
      params: { q, sort, page, limit, from, to },
    });
  },
  async remove(id) {
    return request('delete', `/api/analysis/${id}`);
  },
};
