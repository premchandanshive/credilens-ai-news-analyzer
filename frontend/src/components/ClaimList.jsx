import ClaimCard from './ClaimCard.jsx';

export default function ClaimList({ claims }) {
  const items = claims || [];
  return (
    <section className="card-surface p-5">
      <h2 className="text-sm font-semibold mb-3">Claim Verification</h2>
      {items.length === 0 ? (
        <p className="text-sm text-muted">Extracted claims and evidence statuses will appear after analysis.</p>
      ) : (
        <div className="space-y-2">
          {items.map((claim) => (
            <ClaimCard key={claim.id || claim.text} claim={claim} />
          ))}
        </div>
      )}
    </section>
  );
}
