import { Bell, Menu, Moon, Sun } from 'lucide-react';
import { useState } from 'react';
import { useAuth } from '../hooks/useAuth.js';
import { useAnalysis } from '../hooks/useAnalysis.js';
import { useTheme } from '../hooks/useTheme.js';
import { formatDate } from '../utils/formatters.js';

export default function Topbar({ title, subtitle, onMenu }) {
  const { theme, toggleTheme } = useTheme();
  const { user } = useAuth();
  const { notifications, markNotificationsRead } = useAnalysis();
  const [open, setOpen] = useState(false);
  const unread = notifications.filter((n) => !n.read).length;

  return (
    <header className="sticky top-0 z-20 flex items-start justify-between gap-3 border-b border-cred-border bg-cred-bg/90 px-4 py-4 backdrop-blur lg:px-8">
      <div className="flex items-start gap-3 min-w-0">
        <button
          type="button"
          className="lg:hidden mt-0.5 rounded-lg border border-cred-border p-2 text-cred-muted"
          onClick={onMenu}
          aria-label="Open menu"
        >
          <Menu size={18} />
        </button>
        <div className="min-w-0">
          <h1 className="truncate text-lg font-semibold lg:text-xl">{title}</h1>
          {subtitle ? <p className="mt-0.5 truncate text-xs text-muted lg:text-sm">{subtitle}</p> : null}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={toggleTheme}
          className="rounded-full border border-cred-border p-2 text-cred-muted hover:text-cred-text"
          aria-label="Toggle theme"
        >
          {theme === 'light' ? <Sun size={16} /> : <Moon size={16} />}
        </button>

        <div className="relative">
          <button
            type="button"
            onClick={() => {
              setOpen((v) => !v);
              markNotificationsRead();
            }}
            className="relative rounded-full border border-cred-border p-2 text-cred-muted hover:text-cred-text"
            aria-label="Notifications"
          >
            <Bell size={16} />
            {unread > 0 ? (
              <span className="absolute -right-0.5 -top-0.5 h-4 min-w-4 rounded-full bg-cred-accent px-1 text-[10px] text-white">
                {unread}
              </span>
            ) : null}
          </button>
          {open ? (
            <div className="absolute right-0 mt-2 w-72 card-surface p-2 shadow-xl">
              <p className="px-2 py-1 text-xs font-medium text-muted">Notifications</p>
              {notifications.length === 0 ? (
                <p className="px-2 py-4 text-sm text-muted">No analysis events yet.</p>
              ) : (
                <ul className="max-h-64 overflow-auto">
                  {notifications.map((n) => (
                    <li key={n.id} className="rounded-lg px-2 py-2 text-sm hover:bg-cred-elevated">
                      <p className="font-medium">{n.title}</p>
                      <p className="text-xs text-muted">{n.body}</p>
                      <p className="text-[11px] text-muted">{formatDate(n.createdAt)}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : null}
        </div>

        <div className="hidden sm:flex items-center gap-2 rounded-full border border-cred-border pl-1 pr-3 py-1">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-cred-accent text-xs font-semibold">
            {(user?.displayName || 'G').slice(0, 1).toUpperCase()}
          </div>
          <span className="max-w-[8rem] truncate text-sm">{user?.displayName || 'Guest'}</span>
        </div>
      </div>
    </header>
  );
}
