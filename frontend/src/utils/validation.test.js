import { describe, expect, it } from 'vitest';
import { validateFile, validateText, validateUrl } from './validation.js';

describe('validateText', () => {
  it('rejects empty input', () => {
    expect(validateText('  ')).toBeTruthy();
  });
  it('rejects short input', () => {
    expect(validateText('too short')).toBeTruthy();
  });
  it('accepts a reasonable article', () => {
    expect(validateText('Scientists announced a new study about vaccine effectiveness today.')).toBeNull();
  });
});

describe('validateUrl', () => {
  it('requires http(s)', () => {
    expect(validateUrl('ftp://example.com')).toBeTruthy();
    expect(validateUrl('https://www.example.com/news')).toBeNull();
  });
});

describe('validateFile', () => {
  it('rejects missing file', () => {
    expect(validateFile(null)).toBeTruthy();
  });
  it('rejects unsupported types', () => {
    expect(validateFile({ name: 'photo.png', size: 10 })).toBeTruthy();
  });
  it('accepts txt under size limit', () => {
    expect(validateFile({ name: 'article.txt', size: 100 })).toBeNull();
  });
});
