import { claimStatusLabel } from '../utils/formatters.js';

const TONE = {
  SUPPORTED: 'bg-cred-success/15 text-cred-success',
  CONTRADICTED: 'bg-cred-danger/15 text-cred-danger',
  INSUFFICIENT_EVIDENCE: 'bg-cred-warning/15 text-cred-warning',
};

export default function ClaimCard({ claim }) {
  return (
    <article className="rounded-xl border border-cred-border p-3">
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm">{claim.text}</p>
        <span className={`shrink-0 rounded-md px-2 py-1 text-[11px] font-medium ${TONE[claim.status] || TONE.INSUFFICIENT_EVIDENCE}`}>
          {claimStatusLabel(claim.status)}
        </span>
      </div>
    </article>
  );
}
