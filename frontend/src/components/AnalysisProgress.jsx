import { Check, Circle, Loader2 } from 'lucide-react';
import { ANALYSIS_STAGES } from '../utils/scoreLabels.js';

export default function AnalysisProgress({ progress }) {
  const current = progress?.stage;
  const completed = new Set(progress?.completed || []);
  const failed = current === 'failed';

  return (
    <div className="card-surface p-5">
      <h2 className="text-sm font-semibold">Analyzing your information</h2>
      <p className="mt-1 text-xs text-muted">
        Stages complete only when the backend reports them. They are not simulated.
      </p>
      <ol className="mt-4 space-y-3">
        {ANALYSIS_STAGES.map((item) => {
          const isDone = completed.has(item.stage);
          const isCurrent = current === item.stage && !isDone;
          return (
            <li key={item.stage} className="flex items-center gap-3 text-sm">
              {isDone ? (
                <Check size={16} className="text-cred-success" />
              ) : isCurrent ? (
                <Loader2 size={16} className="animate-spin text-cred-accent" />
              ) : (
                <Circle size={14} className="text-cred-border-strong" />
              )}
              <span className={isDone || isCurrent ? 'text-cred-text' : 'text-muted'}>{item.label}</span>
            </li>
          );
        })}
      </ol>
      {progress?.label ? <p className="mt-3 text-xs text-muted">{progress.label}</p> : null}
      {failed ? <p className="mt-3 text-sm text-cred-danger">Analysis stopped before completion.</p> : null}
    </div>
  );
}
