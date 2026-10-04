import { scoreColorClass } from '../utils/formatters.js';

export default function ScoreCard({ title, description, score, icon: Icon }) {
  const numeric = Number.isFinite(Number(score)) ? Math.round(Number(score)) : null;
  const ratio = numeric == null ? 0 : numeric / 100;
  const tone =
    numeric == null ? 'Moderate' : numeric >= 70 ? 'Good' : numeric >= 45 ? 'Moderate' : 'Weak';
  const toneClass =
    numeric == null ? 'text-muted' : numeric >= 70 ? 'text-cred-success' : numeric >= 45 ? 'text-cred-warning' : 'text-cred-danger';

  return (
    <article className="card-surface p-4 h-full">
      <div className="flex items-start gap-3">
        {Icon ? (
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-cred-accent-soft text-cred-accent">
            <Icon size={16} />
          </div>
        ) : null}
        <div>
          <h3 className="text-sm font-semibold">{title}</h3>
          <p className="mt-1 text-xs text-muted">{description}</p>
        </div>
      </div>
      <div className="mt-6 flex items-center justify-between">
        <div className="relative h-14 w-14">
          <svg viewBox="0 0 36 36" className="-rotate-90">
            <circle cx="18" cy="18" r="14" fill="none" stroke="currentColor" className="text-cred-border" strokeWidth="3" />
            <circle
              cx="18"
              cy="18"
              r="14"
              fill="none"
              stroke="currentColor"
              className={scoreColorClass(numeric ?? 0).replace('text-', 'text-')}
              strokeWidth="3"
              strokeDasharray={`${ratio * 88} 88`}
              strokeLinecap="round"
            />
          </svg>
        </div>
        <div className="text-right">
          <p className={`text-lg font-semibold ${scoreColorClass(numeric ?? NaN)}`}>
            {numeric == null ? '—' : `${numeric}/100`}
          </p>
          <p className={`text-xs ${toneClass}`}>{numeric == null ? 'Pending' : tone}</p>
        </div>
      </div>
    </article>
  );
}
