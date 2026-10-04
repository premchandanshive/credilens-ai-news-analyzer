import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth.js';
import { useTheme } from '../hooks/useTheme.js';
import { useSystemStatus } from '../hooks/useSystemStatus.js';
import { DISCLAIMER } from '../utils/scoreLabels.js';

export default function SettingsPage() {
  const { user, prefs, updatePreferences, updateProfile, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const sys = useSystemStatus();
  const [name, setName] = useState(user?.displayName || '');
  const [saved, setSaved] = useState(false);

  async function onSave(event) {
    event.preventDefault();
    await updatePreferences({
      theme,
      maxClaims: Number(prefs.maxClaims) || 8,
      includeTransformer: Boolean(prefs.includeTransformer),
    });
    await updateProfile({ displayName: name });
    setSaved(true);
  }

  const flags = sys.status || {};

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <form onSubmit={onSave} className="card-surface p-5 space-y-4">
        <h2 className="text-sm font-semibold">Profile & preferences</h2>
        <label className="block text-sm">
          Display name
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2"
          />
        </label>
        <label className="block text-sm">
          Theme
          <select
            value={theme}
            onChange={(e) => {
              setTheme(e.target.value);
              updatePreferences({ theme: e.target.value });
            }}
            className="mt-1 w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2"
          >
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </label>
        <label className="block text-sm">
          Max claims to extract
          <input
            type="number"
            min={1}
            max={20}
            value={prefs.maxClaims}
            onChange={(e) => updatePreferences({ maxClaims: Number(e.target.value) })}
            className="mt-1 w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2"
          />
        </label>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={prefs.includeTransformer}
            onChange={(e) => updatePreferences({ includeTransformer: e.target.checked })}
          />
          Prefer transformer classifier when the backend has it loaded
        </label>
        <button type="submit" className="rounded-xl bg-cred-accent px-4 py-2 text-sm text-white">
          Save preferences
        </button>
        {saved ? <p className="text-xs text-cred-success">Saved locally{user ? ' and queued for profile sync' : ''}.</p> : null}
        <div className="flex gap-3 text-sm">
          {user ? (
            <button type="button" onClick={logout} className="text-cred-danger">
              Log out
            </button>
          ) : (
            <>
              <Link to="/login" className="text-cred-accent">
                Sign in
              </Link>
              <Link to="/register" className="text-muted">
                Create account
              </Link>
            </>
          )}
        </div>
      </form>

      <section className="card-surface p-5 space-y-3">
        <h2 className="text-sm font-semibold">API & system status</h2>
        <StatusRow label="API" ok={sys.online} loading={sys.loading} />
        <StatusRow label="Database" ok={flags.database} />
        <StatusRow label="Models loaded" ok={flags.models} />
        <StatusRow label="NLP pipeline" ok={flags.nlp} />
        <StatusRow label="Evidence providers" ok={flags.evidence} />
        <StatusRow label="Search API key configured" ok={flags.searchKeyConfigured} />
        {!sys.online ? (
          <p className="text-sm text-cred-warning">
            Backend offline. Start FastAPI on the URL in VITE_API_BASE_URL (default proxy: /api → localhost:8000).
          </p>
        ) : null}
        <div className="pt-4 border-t border-cred-border">
          <h3 className="text-sm font-semibold">Scoring methodology</h3>
          <p className="mt-2 text-sm text-muted">{DISCLAIMER}</p>
          <p className="mt-2 text-xs text-muted">
            Default weights: AI 30%, evidence 30%, source 20%, language 10%, claim consistency 10%. Weights are configurable and not scientifically proven.
          </p>
        </div>
      </section>
    </div>
  );
}

function StatusRow({ label, ok, loading }) {
  const text = loading ? 'Checking' : ok ? 'Available' : ok === false ? 'Unavailable' : 'Unknown';
  const color = loading ? 'text-cred-warning' : ok ? 'text-cred-success' : ok === false ? 'text-cred-danger' : 'text-muted';
  return (
    <div className="flex items-center justify-between text-sm">
      <span>{label}</span>
      <span className={color}>{text}</span>
    </div>
  );
}
