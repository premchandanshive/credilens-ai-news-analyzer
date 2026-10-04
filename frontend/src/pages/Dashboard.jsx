import AnalysisInput from '../components/AnalysisInput.jsx';
import AnalysisProgress from '../components/AnalysisProgress.jsx';
import CredibilityGauge from '../components/CredibilityGauge.jsx';
import AnalysisBreakdown from '../components/AnalysisBreakdown.jsx';
import KeyFindings from '../components/KeyFindings.jsx';
import SourceList from '../components/SourceList.jsx';
import ClaimList from '../components/ClaimList.jsx';
import LanguageAnalysis from '../components/LanguageAnalysis.jsx';
import { ComponentScoreChart, ClaimDistributionChart } from '../components/ScoreCharts.jsx';
import { ErrorState } from '../components/ErrorState.jsx';
import { useAnalysis } from '../hooks/useAnalysis.js';

export default function DashboardPage() {
  const { current, status, error, progress, runAnalyze } = useAnalysis();

  return (
    <div className="space-y-5">
      <div className="grid gap-4 xl:grid-cols-[minmax(0,1.4fr)_minmax(280px,0.8fr)]">
        <AnalysisInput onSubmit={(payload) => runAnalyze(payload.kind, payload)} disabled={status === 'analyzing'} compact />
        {status === 'analyzing' ? (
          <AnalysisProgress progress={progress} />
        ) : (
          <CredibilityGauge
            score={current?.credibilityScore}
            band={current?.credibilityBand}
            disclaimer={current?.disclaimer}
          />
        )}
      </div>

      {status === 'error' && error ? <ErrorState error={error} title="Analysis could not be completed" /> : null}

      <AnalysisBreakdown scores={current?.componentScores} />

      <div className="grid gap-4 lg:grid-cols-2">
        <KeyFindings findings={current?.explanation?.findings} analysisId={current?.id} />
        <SourceList sources={current?.sources} analysisId={current?.id} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ClaimList claims={current?.claims} />
        <LanguageAnalysis analysis={current?.languageAnalysis} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ComponentScoreChart scores={current?.componentScores} />
        <ClaimDistributionChart claims={current?.claims} />
      </div>
    </div>
  );
}
