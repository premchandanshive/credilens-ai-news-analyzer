const URL_PATTERN = /^https?:\/\/[^\s]+$/i;
const ALLOWED_EXTENSIONS = ['.txt', '.md', '.pdf'];
export const MAX_TEXT_LENGTH = 50000;
export const MAX_FILE_BYTES = 5 * 1024 * 1024;

export function validateText(text) {
  const value = (text ?? '').trim();
  if (!value) return 'Enter a news article, claim, or paste text to analyze.';
  if (value.length < 20) return 'Provide at least 20 characters so the analyzer has enough context.';
  if (value.length > MAX_TEXT_LENGTH) return `Text exceeds the ${MAX_TEXT_LENGTH.toLocaleString()} character limit.`;
  return null;
}

export function validateUrl(url) {
  const value = (url ?? '').trim();
  if (!value) return 'Paste a news article URL.';
  if (!URL_PATTERN.test(value)) return 'URL must start with http:// or https://.';
  try {
    const parsed = new URL(value);
    if (!['http:', 'https:'].includes(parsed.protocol)) return 'Only http and https URLs are supported.';
  } catch {
    return 'That URL is not valid.';
  }
  return null;
}

export function validateFile(file) {
  if (!file) return 'Choose a supported file (.txt, .md, or .pdf).';
  const name = file.name.toLowerCase();
  const okType = ALLOWED_EXTENSIONS.some((ext) => name.endsWith(ext));
  if (!okType) return 'Unsupported file type. Use .txt, .md, or .pdf.';
  if (file.size > MAX_FILE_BYTES) return 'File is larger than 5 MB.';
  return null;
}

export function looksLikeUrl(value) {
  return /^https?:\/\//i.test((value ?? '').trim());
}
