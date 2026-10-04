import { request } from './apiClient.js';

export const sourceService = {
  async getById(id) {
    return request('get', `/api/sources/${id}`);
  },
};
