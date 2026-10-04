import { useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { NAV } from './Sidebar.jsx';
import { useAuth } from '../hooks/useAuth.js';

export default function MobileDrawer({ open, onClose }) {
  const { user } = useAuth();

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  if (!open) return null;

  return (
    <div className="lg:hidden fixed inset-0 z-40">
      <button className="absolute inset-0 bg-black/50" aria-label="Close menu" onClick={onClose} />
      <div className="absolute left-0 top-0 h-full w-[80%] max-w-xs bg-cred-sidebar border-r border-cred-border p-4">
        <p className="mb-4 text-sm font-semibold">CrediLens</p>
        <nav className="space-y-1">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm ${
                  isActive ? 'bg-cred-accent text-white' : 'text-cred-muted'
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <p className="mt-6 text-xs text-muted">{user?.displayName || 'Guest session'}</p>
      </div>
    </div>
  );
}
