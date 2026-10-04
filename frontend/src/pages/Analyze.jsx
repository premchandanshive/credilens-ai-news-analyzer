import { useNavigate } from 'react-router-dom';
import AnalysisInput from '../components/AnalysisInput.jsx';
import AnalysisProgress from '../components/AnalysisProgress.jsx';
import { ErrorState } from '../components/ErrorState.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';

export default function AnalyzePage() {
  const { status, error, progress, runAnalyze } = useAnalysis();
  const navigate = useNavigate();

  async function onSubmit(payload) {
    const result = await runAnalyze(payload.kind, payload);
    if (result?.success && result.data?.id) {
      navigate(`/analysis/${result.data.id}`);
    } else if (result?.success) {
      navigate('/');
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <AnalysisInput onSubmit={onSubmit} disabled={status === 'analyzing'} />
      {status === 'analyzing' ? <AnalysisProgress progress={progress} /> : null}
      {status === 'error' && error ? <ErrorState error={error} title="Analysis could not be completed" /> : null}
    </div>
  );
}
