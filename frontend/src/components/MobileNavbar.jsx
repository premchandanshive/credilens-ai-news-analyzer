import { NavLink } from 'react-router-dom';
import { History, Home, Newspaper, Search } from 'lucide-react';

const ITEMS = [
  { to: '/', label: 'Home', icon: Home, end: true },
  { to: '/analyze', label: 'Analyze', icon: Search },
  { to: '/history', label: 'History', icon: History },
  { to: '/sources', label: 'Sources', icon: Newspaper },
];

export default function MobileNavbar() {
  return (
    <nav className="lg:hidden fixed bottom-0 inset-x-0 z-30 border-t border-cred-border bg-cred-sidebar/95 backdrop-blur">
      <ul className="grid grid-cols-4">
        {ITEMS.map((item) => (
          <li key={item.to}>
            <NavLink
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 py-3 text-[11px] ${
                  isActive ? 'text-cred-accent' : 'text-cred-muted'
                }`
              }
            >
              <item.icon size={18} />
              {item.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
