import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout.jsx';
import { useAuth } from '../hooks/useAuth.js';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [pending, setPending] = useState(false);

  async function onSubmit(event) {
    event.preventDefault();
    setPending(true);
    setError(null);
    const result = await register({ email, password, displayName });
    setPending(false);
    if (result.success) navigate('/');
    else setError(result.error);
  }

  return (
    <AuthLayout
      title="Create account"
      footer={
        <p className="mt-4 text-sm text-muted">
          Already registered? <Link to="/login" className="text-cred-accent">Sign in</Link>
        </p>
      }
    >
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          required
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          placeholder="Display name"
          className="w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2 text-sm"
        />
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2 text-sm"
        />
        <input
          type="password"
          required
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password (min 8 characters)"
          className="w-full rounded-xl border border-cred-border bg-cred-bg px-3 py-2 text-sm"
        />
        {error ? <p className="text-sm text-cred-danger">{error.message}</p> : null}
        <button disabled={pending} className="w-full rounded-xl bg-cred-accent py-2 text-sm text-white disabled:opacity-50">
          {pending ? 'Creating…' : 'Register'}
        </button>
      </form>
    </AuthLayout>
  );
}
