import { FileQuestion, Inbox, ServerOff } from 'lucide-react';

export default function EmptyState({ title, description, action }) {
  return (
    <div className="card-surface flex flex-col items-center justify-center px-6 py-12 text-center">
      <Inbox className="text-muted mb-3" size={28} />
      <h2 className="text-sm font-semibold">{title}</h2>
      <p className="mt-2 max-w-md text-sm text-muted">{description}</p>
      {action}
    </div>
  );
}

export function ErrorState({ title = 'Unable to complete this action', error, onRetry }) {
  const offline = error?.code === 'BACKEND_UNAVAILABLE';
  const Icon = offline ? ServerOff : FileQuestion;
  return (
    <div className="card-surface flex flex-col items-center justify-center px-6 py-10 text-center">
      <Icon className="text-cred-danger mb-3" size={28} />
      <h2 className="text-sm font-semibold">{title}</h2>
      <p className="mt-2 max-w-md text-sm text-muted">{error?.message || 'Please try again.'}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry} className="mt-4 rounded-xl bg-cred-accent px-4 py-2 text-sm text-white">
          Retry
        </button>
      ) : null}
    </div>
  );
}

export function LoadingState({ label = 'Loading…' }) {
  return (
    <div className="card-surface px-6 py-10 text-center text-sm text-muted">
      <div className="mx-auto mb-3 h-6 w-6 animate-spin rounded-full border-2 border-cred-border border-t-cred-accent" />
      {label}
    </div>
  );
}
