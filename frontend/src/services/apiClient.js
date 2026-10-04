import axios from 'axios';
import { storage } from '../utils/storage.js';

const baseURL = import.meta.env.VITE_API_BASE_URL ?? '';

export const apiClient = axios.create({
  baseURL,
  timeout: 90000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config) => {
  const token = storage.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  }
  return config;
});

function normalizeAxiosError(error) {
  if (error.code === 'ECONNABORTED') {
    return { code: 'TIMEOUT', message: 'The request timed out. Try a shorter article or try again.' };
  }
  if (!error.response) {
    return {
      code: 'BACKEND_UNAVAILABLE',
      message: 'The analyzer backend is not reachable. Start the FastAPI server and check VITE_API_BASE_URL.',
    };
  }
  const payload = error.response.data;
  if (payload?.error?.code) return payload.error;
  if (error.response.status === 413) {
    return { code: 'PAYLOAD_TOO_LARGE', message: 'That input is too large to analyze.' };
  }
  if (error.response.status === 401) {
    return { code: 'UNAUTHORIZED', message: 'Please sign in to continue.' };
  }
  return {
    code: 'INTERNAL',
    message: payload?.error?.message || 'The server could not complete this request.',
  };
}

export async function request(method, url, { data, params, headers, timeout } = {}) {
  try {
    const response = await apiClient.request({ method, url, data, params, headers, timeout });
    const body = response.data;
    if (body && typeof body.success === 'boolean') {
      if (body.success) return { success: true, data: body.data, error: null };
      return { success: false, data: null, error: body.error || { code: 'INTERNAL', message: 'Request failed.' } };
    }
    return { success: true, data: body, error: null };
  } catch (error) {
    return { success: false, data: null, error: normalizeAxiosError(error) };
  }
}

export function apiUrl(path) {
  const root = (baseURL || '').replace(/\/$/, '');
  if (path.startsWith('http')) return path;
  return `${root}${path}`;
}
