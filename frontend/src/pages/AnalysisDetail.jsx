import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import DashboardPage from './Dashboard.jsx';
import { LoadingState, ErrorState } from '../components/EmptyState.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';

export default function AnalysisDetailPage() {
  const { id } = useParams();
  const { loadById, status, error, current } = useAnalysis();

  useEffect(() => {
    if (id) loadById(id);
  }, [id, loadById]);

  if (status === 'loading' && !current) return <LoadingState label="Opening saved analysis…" />;
  if (status === 'error' && error) return <ErrorState error={error} title="Could not open this analysis" />;
  return <DashboardPage />;
}
