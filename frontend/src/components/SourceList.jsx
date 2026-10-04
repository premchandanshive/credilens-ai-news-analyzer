import { Link } from 'react-router-dom';
import SourceCard from './SourceCard.jsx';

export default function SourceList({ sources, analysisId }) {
  const items = sources || [];
  return (
    <section className="card-surface p-5 h-full">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold">Top Matched Sources</h2>
        {analysisId ? (
          <Link to="/sources" className="text-xs text-cred-accent">
            View all
          </Link>
        ) : (
          <span className="text-xs text-muted">View all</span>
        )}
      </div>
      {items.length === 0 ? (
        <p className="text-sm text-muted">Matched sources will list here with live URLs from the evidence service.</p>
      ) : (
        <div className="space-y-2">
          {items.slice(0, 5).map((source, i) => (
            <SourceCard key={source.url || i} source={source} index={i + 1} />
          ))}
        </div>
      )}
    </section>
  );
}
