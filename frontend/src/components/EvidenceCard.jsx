export default function EvidenceCard({ item }) {
  return (
    <article className="rounded-xl border border-cred-border p-3">
      <a href={item.url} className="text-sm font-medium text-cred-accent" target="_blank" rel="noreferrer">
        {item.title}
      </a>
      <p className="mt-1 text-xs text-muted">{item.snippet || item.excerpt}</p>
    </article>
  );
}
