import { apiUrl, request } from './apiClient.js';
import { storage } from '../utils/storage.js';

const STAGE_ORDER = [
  'extracting_article',
  'analyzing_text',
  'extracting_claims',
  'searching_evidence',
  'evaluating_sources',
  'calculating_credibility',
  'generating_explanation',
];

function normalizeAnalysis(raw) {
  if (!raw) return null;
  return {
    ...raw,
    id: raw.id || raw._id,
    claims: raw.claims || [],
    sources: raw.sources || [],
    explanation: raw.explanation || { findings: [], modelExplanation: { method: 'unavailable', topFeatures: [] } },
    componentScores: raw.componentScores || {
      aiClassification: null,
      evidenceVerification: null,
      sourceAnalysis: null,
      languageAnalysis: null,
      claimConsistency: null,
    },
  };
}

async function consumeSse(url, onEvent) {
  const token = storage.getToken();
  const response = await fetch(url, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!response.ok || !response.body) {
    throw new Error('Progress stream unavailable');
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split('\n\n');
    buffer = chunks.pop() ?? '';
    for (const chunk of chunks) {
      const line = chunk.split('\n').find((l) => l.startsWith('data:'));
      if (!line) continue;
      try {
        const payload = JSON.parse(line.slice(5).trim());
        onEvent(payload);
      } catch {
        /* ignore malformed event */
      }
    }
  }
}

/**
 * Subscribe to backend progress. Does not invent completed stages.
 */
export async function subscribeProgress(analysisId, onEvent) {
  const url = apiUrl(`/api/analyze/${analysisId}/events`);
  try {
    await consumeSse(url, onEvent);
  } catch {
    onEvent({ stage: 'progress_unavailable', label: 'Waiting for backend progress…', done: false });
  }
}

export const analysisService = {
  async analyzeText(text, title) {
    return request('post', '/api/analyze/text', { data: { text, title } });
  },
  async analyzeUrl(url) {
    return request('post', '/api/analyze/url', { data: { url } });
  },
  async analyzeFile(file) {
    const form = new FormData();
    form.append('file', file);
    return request('post', '/api/analyze/file', { data: form });
  },
  async getById(id) {
    const result = await request('get', `/api/analysis/${id}`);
    if (result.success) result.data = normalizeAnalysis(result.data);
    return result;
  },
  async getReport(id) {
    return request('get', `/api/analysis/${id}/report`);
  },
  stageOrder: STAGE_ORDER,
};
