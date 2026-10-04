export function formatDate(iso) {
  if (!iso) return '—';
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}

export function formatDomain(urlOrDomain) {
  if (!urlOrDomain) return 'Unknown source';
  try {
    if (urlOrDomain.includes('://')) return new URL(urlOrDomain).hostname.replace(/^www\./, '');
    return urlOrDomain.replace(/^www\./, '');
  } catch {
    return urlOrDomain;
  }
}

export function scoreColorClass(score) {
  const n = Number(score);
  if (!Number.isFinite(n)) return 'text-cred-muted';
  if (n >= 61) return 'text-cred-success';
  if (n >= 41) return 'text-cred-warning';
  return 'text-cred-danger';
}

export function relationshipLabel(rel) {
  switch (rel) {
    case 'supports':
      return 'Supports';
    case 'contradicts':
      return 'Contradicts';
    case 'related':
      return 'Related';
    default:
      return 'Insufficient';
  }
}

export function claimStatusLabel(status) {
  switch (status) {
    case 'SUPPORTED':
      return 'Supported';
    case 'CONTRADICTED':
      return 'Contradicted';
    default:
      return 'Insufficient evidence';
  }
}

export function userMessageFromError(error) {
  if (!error) return 'Something went wrong. Please try again.';
  if (typeof error === 'string') return error;
  return error.message || 'Something went wrong. Please try again.';
}
