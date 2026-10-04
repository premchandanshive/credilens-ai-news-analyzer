import { describe, expect, it } from 'vitest';
import { bandForScore } from './scoreLabels.js';

describe('bandForScore', () => {
  it('maps 0-100 into documented bands', () => {
    expect(bandForScore(10).key).toBe('highly_unreliable');
    expect(bandForScore(30).key).toBe('likely_misleading');
    expect(bandForScore(50).key).toBe('uncertain');
    expect(bandForScore(72).key).toBe('likely_reliable');
    expect(bandForScore(90).key).toBe('highly_reliable');
  });
  it('does not invent a score for missing values', () => {
    expect(bandForScore(undefined).key).toBe('unknown');
  });
});
