import { Link } from 'react-router-dom';

export default function AuthLayout({ title, children, footer }) {
  return (
    <div className="min-h-screen bg-cred-bg text-cred-text flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Link to="/" className="mb-6 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cred-accent font-semibold">C</div>
          <div>
            <p className="font-semibold">CrediLens</p>
            <p className="text-xs text-muted">AI News Analyzer</p>
          </div>
        </Link>
        <div className="card-surface p-6">
          <h1 className="text-xl font-semibold mb-4">{title}</h1>
          {children}
        </div>
        {footer}
      </div>
    </div>
  );
}
