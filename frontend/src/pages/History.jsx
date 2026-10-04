import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import EmptyState from '../components/EmptyState.jsx';
import { ErrorState, LoadingState } from '../components/EmptyState.jsx';
import HistoryTable from '../components/HistoryTable.jsx';
import { HistoryTrendChart } from '../components/ScoreCharts.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';
import { historyService } from '../services/historyService.js';

export default function HistoryPage() {
  const { history, historyMeta, loadHistory, loadById } = useAnalysis();
  const [q, setQ] = useState('');
  const [sort, setSort] = useState('createdAt_desc');
  const navigate = useNavigate();

  useEffect(() => {
    loadHistory({ q, sort });
  }, [loadHistory, sort]);

  function search(event) {
    event.preventDefault();
    loadHistory({ q, sort });
  }

  async function onDelete(item) {
    const id = item.id || item._id;
    if (!id) return;
    const confirmed = window.confirm('Delete this analysis from history?');
    if (!confirmed) return;
    const result = await historyService.remove(id);
    if (!result.success) {
      window.alert(result.error?.message || 'Could not delete.');
      return;
    }
    loadHistory({ q, sort });
  }

  async function onOpen(item) {
    const id = item.id || item._id;
    await loadById(id);
    navigate(`/analysis/${id}`);
  }

  return (
    <div className="space-y-4">
      <form onSubmit={search} className="flex flex-col gap-3 sm:flex-row">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Search title or excerpt"
          className="flex-1 rounded-xl border border-cred-border bg-cred-card px-3 py-2 text-sm"
        />
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="rounded-xl border border-cred-border bg-cred-card px-3 py-2 text-sm"
        >
          <option value="createdAt_desc">Newest</option>
          <option value="createdAt_asc">Oldest</option>
          <option value="score_desc">Highest score</option>
          <option value="score_asc">Lowest score</option>
        </select>
        <button type="submit" className="rounded-xl bg-cred-accent px-4 py-2 text-sm text-white">
          Search
        </button>
      </form>

      {historyMeta.loading ? <LoadingState label="Loading history…" /> : null}
      {historyMeta.error ? (
        <ErrorState title="History is unavailable" error={historyMeta.error} onRetry={() => loadHistory({ q, sort })} />
      ) : null}
      {!historyMeta.loading && !historyMeta.error && history.items.length === 0 ? (
        <EmptyState
          title="No saved analyses"
          description="Completed assessments are stored in MongoDB. Run an analysis to populate history."
        />
      ) : null}

      <HistoryTrendChart items={history.items} />
      <HistoryTable items={history.items} onDelete={onDelete} onOpen={onOpen} />
    </div>
  );
}
