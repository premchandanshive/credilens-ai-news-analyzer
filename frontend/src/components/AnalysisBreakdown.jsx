import { FileSearch, Languages, ShieldCheck } from 'lucide-react';
import ScoreCard from './ScoreCard.jsx';

export default function AnalysisBreakdown({ scores }) {
  const s = scores || {};
  return (
    <section>
      <h2 className="mb-3 text-sm font-semibold">Analysis Breakdown</h2>
      <div className="grid gap-3 md:grid-cols-3">
        <ScoreCard
          title="Text Analysis"
          description="Language patterns and the AI classifier contribution."
          score={s.languageAnalysis ?? s.aiClassification}
          icon={Languages}
        />
        <ScoreCard
          title="Source Analysis"
          description="Transparency and metadata available on matched sources."
          score={s.sourceAnalysis}
          icon={FileSearch}
        />
        <ScoreCard
          title="Fact Checking"
          description="Evidence support versus contradiction for extracted claims."
          score={s.evidenceVerification}
          icon={ShieldCheck}
        />
      </div>
    </section>
  );
}
