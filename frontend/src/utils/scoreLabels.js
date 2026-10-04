/** @typedef {import('../types/analysis.js')} */

export const DISCLAIMER =
  'This assessment estimates credibility using AI classification, evidence retrieval, source analysis, and linguistic signals. It is not a determination of absolute truth.';

export const CREDIBILITY_BANDS = [
  { min: 0, max: 20, key: 'highly_unreliable', label: 'Highly Unreliable' },
  { min: 21, max: 40, key: 'likely_misleading', label: 'Likely Misleading' },
  { min: 41, max: 60, key: 'uncertain', label: 'Uncertain' },
  { min: 61, max: 80, key: 'likely_reliable', label: 'Likely Reliable' },
  { min: 81, max: 100, key: 'highly_reliable', label: 'Highly Reliable' },
];

export function bandForScore(score) {
  const n = Number(score);
  if (!Number.isFinite(n)) return { key: 'unknown', label: 'No assessment yet' };
  const band = CREDIBILITY_BANDS.find((b) => n >= b.min && n <= b.max);
  return band ?? { key: 'unknown', label: 'No assessment yet' };
}

export function bandTone(key) {
  if (key === 'highly_reliable' || key === 'likely_reliable') return 'success';
  if (key === 'uncertain') return 'warning';
  if (key === 'likely_misleading' || key === 'highly_unreliable') return 'danger';
  return 'muted';
}

export const ANALYSIS_STAGES = [
  { stage: 'extracting_article', label: 'Extracting article...' },
  { stage: 'analyzing_text', label: 'Analyzing text...' },
  { stage: 'extracting_claims', label: 'Extracting claims...' },
  { stage: 'searching_evidence', label: 'Searching evidence...' },
  { stage: 'evaluating_sources', label: 'Evaluating sources...' },
  { stage: 'calculating_credibility', label: 'Calculating credibility...' },
  { stage: 'generating_explanation', label: 'Generating explanation...' },
];

export function displayBandLabel(result) {
  if (!result) return 'Awaiting analysis';
  const fromScore = bandForScore(result.credibilityScore);
  if (result.credibilityBand) {
    const match = CREDIBILITY_BANDS.find((b) => b.key === result.credibilityBand);
    return match?.label ?? fromScore.label;
  }
  return fromScore.label;
}
