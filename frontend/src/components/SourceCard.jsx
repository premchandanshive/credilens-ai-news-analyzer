import { relationshipLabel, scoreColorClass } from '../utils/formatters.js';

export default function SourceCard({ source, index }) {
  const transparency = Number.isFinite(source.transparencyScore) ? Math.round(source.transparencyScore) : null;
  return (
    <article className="flex flex-col gap-2 rounded-xl border border-cred-border px-3 py-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0">
        <p className="text-sm">
          <span className="text-muted mr-2">{index}.</span>
          <a href={source.url} target="_blank" rel="noreferrer" className="font-medium hover:text-cred-accent">
            {source.title || source.domain}
          </a>
        </p>
        <p className="text-xs text-muted truncate">{source.domain}</p>
        <p className="mt-1 text-xs text-muted line-clamp-2">{source.excerpt}</p>
      </div>
      <div className="flex items-center gap-2 shrink-0">
        <span className="rounded-md bg-cred-elevated px-2 py-1 text-[11px] text-muted">{relationshipLabel(source.relationship)}</span>
        <span className={`text-sm font-semibold ${scoreColorClass(transparency ?? NaN)}`}>
          {transparency == null ? '—' : `${transparency}/100`}
        </span>
      </div>
    </article>
  );
}
