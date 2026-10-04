import { NavLink } from 'react-router-dom';
import {
  FileBarChart2,
  History,
  LayoutDashboard,
  Newspaper,
  Search,
  Settings,
} from 'lucide-react';
import { useAuth } from '../hooks/useAuth.js';
import { useSystemStatus } from '../hooks/useSystemStatus.js';

const NAV = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/analyze', label: 'Analyze News', icon: Search },
  { to: '/history', label: 'History', icon: History },
  { to: '/sources', label: 'Sources', icon: Newspaper },
  { to: '/reports', label: 'Reports', icon: FileBarChart2 },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ onNavigate }) {
  const { user } = useAuth();
  const { online, loading, status } = useSystemStatus();
  const modelOk = status?.models !== false && online;

  return (
    <aside className="hidden lg:flex w-[260px] shrink-0 flex-col border-r border-cred-border bg-cred-sidebar min-h-screen">
      <div className="flex items-center gap-3 px-5 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cred-accent text-white font-semibold">
          C
        </div>
        <div>
          <p className="text-sm font-semibold tracking-wide">CrediLens</p>
          <p className="text-xs text-muted">AI News Analyzer</p>
        </div>
      </div>

      <nav className="flex-1 px-3 space-y-1">
        {NAV.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.end}
            onClick={onNavigate}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors ${
                isActive
                  ? 'bg-cred-accent text-white'
                  : 'text-cred-muted hover:bg-cred-elevated hover:text-cred-text'
              }`
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-4 pb-4 space-y-3">
        <div className="card-surface p-3">
          <p className="text-xs font-medium mb-1">AI Model Status</p>
          <div className="flex items-center gap-2 text-xs">
            <span className={`h-2 w-2 rounded-full ${loading ? 'bg-cred-warning' : online ? 'bg-cred-success' : 'bg-cred-danger'}`} />
            <span className={online ? 'text-cred-success' : 'text-cred-danger'}>
              {loading ? 'Checking' : online ? 'Online' : 'Offline'}
            </span>
          </div>
          <p className="mt-1 text-[11px] text-muted">
            {modelOk ? 'Inference artifacts expected at backend startup.' : 'Connect FastAPI to load classifiers.'}
          </p>
        </div>

        <NavLink
          to="/settings"
          className="card-surface flex items-center gap-3 p-3 hover:bg-cred-card-hover"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-cred-accent text-xs font-semibold">
            {(user?.displayName || user?.email || 'G').slice(0, 1).toUpperCase()}
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium">{user?.displayName || 'Guest'}</p>
            <p className="truncate text-xs text-muted">{user?.role || (user ? 'Signed in' : 'Local session')}</p>
          </div>
        </NavLink>
      </div>
    </aside>
  );
}

export { NAV };
