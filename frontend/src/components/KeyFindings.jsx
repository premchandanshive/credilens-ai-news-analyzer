import { AlertTriangle, Check, Info, XCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const ICONS = {
  positive: Check,
  warning: AlertTriangle,
  negative: XCircle,
  info: Info,
};

const COLORS = {
  positive: 'text-cred-success',
  warning: 'text-cred-warning',
  negative: 'text-cred-danger',
  info: 'text-cred-info',
};

export default function KeyFindings({ findings, analysisId }) {
  const items = findings || [];
  return (
    <section className="card-surface p-5 h-full">
      <h2 className="text-sm font-semibold">Key Findings</h2>
      {items.length === 0 ? (
        <p className="mt-4 text-sm text-muted">Findings appear after a completed analysis.</p>
      ) : (
        <ul className="mt-4 space-y-3">
          {items.map((item, index) => {
            const Icon = ICONS[item.tone] || Info;
            return (
              <li key={`${item.text}-${index}`} className="flex gap-2 text-sm">
                <Icon size={16} className={`mt-0.5 shrink-0 ${COLORS[item.tone] || 'text-muted'}`} />
                <span>{item.text}</span>
              </li>
            );
          })}
        </ul>
      )}
      {analysisId ? (
        <Link to={`/reports?id=${analysisId}`} className="mt-5 inline-flex text-sm text-cred-accent hover:underline">
          View Full Report →
        </Link>
      ) : (
        <p className="mt-5 text-sm text-muted">View Full Report →</p>
      )}
    </section>
  );
}
