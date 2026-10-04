import { useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import EmptyState from '../components/EmptyState.jsx';
import ReportView from '../components/ReportView.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';

export default function ReportsPage() {
  const { current, loadById } = useAnalysis();
  const [params] = useSearchParams();
  const id = params.get('id');

  useEffect(() => {
    if (id && id !== current?.id) {
      loadById(id);
    }
  }, [id, current?.id, loadById]);

  if (!current) {
    return (
      <EmptyState
        title="No report to display"
        description="Complete an analysis or open one from history to generate a report."
        action={
          <Link to="/history" className="mt-4 text-sm text-cred-accent">
            Open history
          </Link>
        }
      />
    );
  }

  return <ReportView analysis={current} />;
}
