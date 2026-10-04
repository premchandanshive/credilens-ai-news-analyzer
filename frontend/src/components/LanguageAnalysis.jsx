export default function LanguageAnalysis({ analysis }) {
  if (!analysis) {
    return (
      <section className="card-surface p-5">
        <h2 className="text-sm font-semibold">Language Analysis</h2>
        <p className="mt-3 text-sm text-muted">
          Sensationalism is a supporting signal. It does not by itself mean the content is fake.
        </p>
      </section>
    );
  }

  return (
    <section className="card-surface p-5">
      <h2 className="text-sm font-semibold">Language Analysis</h2>
      <dl className="mt-4 grid grid-cols-2 gap-3 text-sm">
        <div>
          <dt className="text-xs text-muted">Sensationalism</dt>
          <dd className="font-medium">{analysis.sensationalismScore ?? '—'}/100</dd>
        </div>
        <div>
          <dt className="text-xs text-muted">Emotional language</dt>
          <dd className="font-medium capitalize">{analysis.emotionalLanguage || '—'}</dd>
        </div>
        <div>
          <dt className="text-xs text-muted">Clickbait indicators</dt>
          <dd className="font-medium capitalize">{analysis.clickbaitIndicators || '—'}</dd>
        </div>
        <div>
          <dt className="text-xs text-muted">Absolute claims</dt>
          <dd className="font-medium">{analysis.absoluteClaimCount ?? '—'}</dd>
        </div>
      </dl>
      {analysis.signals?.length ? (
        <ul className="mt-3 list-disc pl-4 text-xs text-muted">
          {analysis.signals.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}
