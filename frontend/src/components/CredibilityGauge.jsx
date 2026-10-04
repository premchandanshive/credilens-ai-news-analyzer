import { Info } from 'lucide-react';
import { bandForScore, bandTone, displayBandLabel } from '../utils/scoreLabels.js';

function polar(cx, cy, r, angleDeg) {
  const rad = ((angleDeg - 180) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function arcPath(cx, cy, r, start, end) {
  const s = polar(cx, cy, r, start);
  const e = polar(cx, cy, r, end);
  const large = end - start > 180 ? 1 : 0;
  return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
}

export default function CredibilityGauge({ score, band, disclaimer }) {
  const numeric = Number.isFinite(Number(score)) ? Math.max(0, Math.min(100, Number(score))) : null;
  const meta = numeric == null ? { key: 'unknown', label: 'Awaiting analysis' } : bandForScore(numeric);
  const label = band ? displayBandLabel({ credibilityScore: numeric, credibilityBand: band }) : meta.label;
  const tone = bandTone(meta.key);
  const toneClass =
    tone === 'success' ? 'text-cred-success' : tone === 'warning' ? 'text-cred-warning' : tone === 'danger' ? 'text-cred-danger' : 'text-muted';

  const sweep = numeric == null ? 0 : (numeric / 100) * 180;

  return (
    <section className="card-surface p-5 h-full">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold">Credibility Assessment</h2>
        <span title={disclaimer || 'Estimates credibility; not absolute truth.'}>
          <Info size={16} className="text-muted" />
        </span>
      </div>
      <div className="mt-2 flex flex-col items-center">
        <svg viewBox="0 0 200 120" className="w-full max-w-[260px]">
          <path d={arcPath(100, 110, 80, 0, 60)} stroke="#f87171" strokeWidth="12" fill="none" strokeLinecap="round" />
          <path d={arcPath(100, 110, 80, 60, 120)} stroke="#fbbf24" strokeWidth="12" fill="none" strokeLinecap="round" />
          <path d={arcPath(100, 110, 80, 120, 180)} stroke="#34d399" strokeWidth="12" fill="none" strokeLinecap="round" />
          <path
            d={arcPath(100, 110, 68, 0, Math.max(1, sweep))}
            stroke="white"
            strokeWidth="3"
            fill="none"
            strokeLinecap="round"
            opacity={numeric == null ? 0 : 0.7}
          />
          <text x="100" y="100" textAnchor="middle" fill="currentColor" className="fill-cred-text" fontSize="28" fontWeight="700">
            {numeric == null ? '—' : numeric}
          </text>
          <text x="100" y="116" textAnchor="middle" fill="#8b95ad" fontSize="11">
            /100
          </text>
        </svg>
        <p className={`mt-1 text-sm font-medium ${toneClass}`}>{label}</p>
        <p className="mt-2 text-center text-xs text-muted max-w-xs">
          {disclaimer ||
            'This assessment estimates credibility using AI classification, evidence retrieval, source analysis, and linguistic signals.'}
        </p>
      </div>
    </section>
  );
}
