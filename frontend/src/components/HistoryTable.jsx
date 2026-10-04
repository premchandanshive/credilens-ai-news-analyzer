import { Link } from 'react-router-dom';
import { formatDate } from '../utils/formatters.js';
import { displayBandLabel } from '../utils/scoreLabels.js';

export default function HistoryTable({ items, onDelete, onOpen }) {
  if (!items?.length) return null;

  return (
    <>
      <div className="hidden md:block overflow-x-auto card-surface">
        <table className="w-full text-sm">
          <thead className="text-left text-xs text-muted border-b border-cred-border">
            <tr>
              <th className="px-4 py-3">Title</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Band</th>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id || item._id} className="border-b border-cred-border/60">
                <td className="px-4 py-3">
                  <Link className="hover:text-cred-accent" to={`/analysis/${item.id || item._id}`}>
                    {item.title || 'Untitled analysis'}
                  </Link>
                </td>
                <td className="px-4 py-3 capitalize text-muted">{item.inputType}</td>
                <td className="px-4 py-3">{item.credibilityScore ?? '—'}</td>
                <td className="px-4 py-3">{displayBandLabel(item)}</td>
                <td className="px-4 py-3 text-muted">{formatDate(item.createdAt)}</td>
                <td className="px-4 py-3 text-right space-x-2">
                  <button type="button" className="text-cred-accent" onClick={() => onOpen(item)}>
                    Open
                  </button>
                  <button type="button" className="text-cred-danger" onClick={() => onDelete(item)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="md:hidden space-y-3">
        {items.map((item) => (
          <article key={item.id || item._id} className="card-surface p-4">
            <Link to={`/analysis/${item.id || item._id}`} className="font-medium">
              {item.title || 'Untitled analysis'}
            </Link>
            <p className="mt-1 text-xs text-muted">
              {item.credibilityScore ?? '—'} · {displayBandLabel(item)} · {formatDate(item.createdAt)}
            </p>
            <div className="mt-3 flex gap-3 text-sm">
              <button type="button" className="text-cred-accent" onClick={() => onOpen(item)}>
                Open
              </button>
              <button type="button" className="text-cred-danger" onClick={() => onDelete(item)}>
                Delete
              </button>
            </div>
          </article>
        ))}
      </div>
    </>
  );
}
