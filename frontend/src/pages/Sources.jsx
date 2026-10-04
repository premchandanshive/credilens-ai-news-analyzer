import { Link } from 'react-router-dom';
import EmptyState from '../components/EmptyState.jsx';
import SourceCard from '../components/SourceCard.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';

export default function SourcesPage() {
  const { current } = useAnalysis();
  const sources = current?.sources || [];

  if (!current) {
    return (
      <EmptyState
        title="No analysis selected"
        description="Open a completed analysis from History or run a new assessment to inspect matched sources."
        action={
          <Link to="/analyze" className="mt-4 text-sm text-cred-accent">
            Analyze news
          </Link>
        }
      />
    );
  }

  return (
    <div className="space-y-3">
      <p className="text-sm text-muted">
        Sources for <span className="text-cred-text">{current.title || 'current analysis'}</span>. Each link opens the original URL.
      </p>
      {sources.length === 0 ? (
        <EmptyState
          title="No sources in this result"
          description="The evidence service did not return matching documents, or evidence was unavailable."
        />
      ) : (
        sources.map((source, i) => <SourceCard key={source.url || i} source={source} index={i + 1} />)
      )}
    </div>
  );
}
