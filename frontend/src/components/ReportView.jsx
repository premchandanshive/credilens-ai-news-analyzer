import { DISCLAIMER } from '../utils/scoreLabels.js';
import { formatDate, claimStatusLabel } from '../utils/formatters.js';
import { displayBandLabel } from '../utils/scoreLabels.js';

export default function ReportView({ analysis }) {
  if (!analysis) return null;

  function downloadJson() {
    const blob = new Blob([JSON.stringify(analysis, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `credilens-report-${analysis.id || 'analysis'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function printReport() {
    window.print();
  }

  return (
    <article className="card-surface p-6 print:border-0 print:bg-white print:text-black">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold">{analysis.title || 'Credibility report'}</h2>
          <p className="text-xs text-muted mt-1">{formatDate(analysis.createdAt)}</p>
        </div>
        <div className="flex gap-2">
          <button type="button" onClick={downloadJson} className="rounded-xl border border-cred-border px-3 py-2 text-sm">
            Download JSON
          </button>
          <button type="button" onClick={printReport} className="rounded-xl bg-cred-accent px-3 py-2 text-sm text-white">
            Download Report
          </button>
        </div>
      </div>

      <p className="mt-4 text-sm text-muted">{analysis.disclaimer || DISCLAIMER}</p>

      <section className="mt-6">
        <h3 className="text-sm font-semibold">Input</h3>
        <p className="mt-2 text-sm whitespace-pre-wrap">{analysis.inputUrl || analysis.inputText || analysis.articleExcerpt || '—'}</p>
      </section>

      <section className="mt-6 grid gap-3 sm:grid-cols-2">
        <div>
          <h3 className="text-sm font-semibold">Credibility score</h3>
          <p className="text-2xl font-semibold mt-1">{analysis.credibilityScore ?? '—'}/100</p>
          <p className="text-sm text-muted">{displayBandLabel(analysis)}</p>
        </div>
        <div>
          <h3 className="text-sm font-semibold">AI prediction</h3>
          <p className="mt-1 text-sm capitalize">{analysis.prediction?.label?.replaceAll('_', ' ') || '—'}</p>
          <p className="text-xs text-muted">{analysis.prediction?.modelName}</p>
        </div>
      </section>

      <section className="mt-6">
        <h3 className="text-sm font-semibold">Claims</h3>
        <ul className="mt-2 space-y-2 text-sm">
          {(analysis.claims || []).map((c) => (
            <li key={c.id || c.text}>
              {c.text} — {claimStatusLabel(c.status)}
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-6">
        <h3 className="text-sm font-semibold">Sources</h3>
        <ul className="mt-2 space-y-2 text-sm">
          {(analysis.sources || []).map((s) => (
            <li key={s.url}>
              <a className="text-cred-accent" href={s.url} target="_blank" rel="noreferrer">
                {s.title}
              </a>
              <span className="text-muted"> — {s.excerpt}</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-6">
        <h3 className="text-sm font-semibold">Explanation</h3>
        <ul className="mt-2 list-disc pl-5 text-sm">
          {(analysis.explanation?.findings || []).map((f) => (
            <li key={f.text}>{f.text}</li>
          ))}
        </ul>
      </section>
    </article>
  );
}
