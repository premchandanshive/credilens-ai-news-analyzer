import { request } from './apiClient.js';
import { storage } from '../utils/storage.js';

export const authService = {
  async register({ email, password, displayName }) {
    const result = await request('post', '/api/auth/register', { data: { email, password, displayName } });
    if (result.success && result.data?.token) storage.setToken(result.data.token);
    return result;
  },
  async login({ email, password }) {
    const result = await request('post', '/api/auth/login', { data: { email, password } });
    if (result.success && result.data?.token) storage.setToken(result.data.token);
    return result;
  },
  async logout() {
    await request('post', '/api/auth/logout');
    storage.setToken(null);
    return { success: true, data: null, error: null };
  },
  async me() {
    return request('get', '/api/auth/me');
  },
  async updateMe(payload) {
    return request('patch', '/api/auth/me', { data: payload });
  },
};
