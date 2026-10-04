import { Link, Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';
import Sidebar from '../components/Sidebar.jsx';
import Topbar from '../components/Topbar.jsx';
import MobileNavbar from '../components/MobileNavbar.jsx';
import MobileDrawer from '../components/MobileDrawer.jsx';

const META = {
  '/': {
    title: 'Dashboard',
    subtitle: 'Analyze news, detect misinformation, and stay informed.',
  },
  '/analyze': {
    title: 'Analyze News',
    subtitle: 'Submit text, a URL, or a document for a credibility assessment.',
  },
  '/history': {
    title: 'History',
    subtitle: 'Search and reopen previous assessments stored in MongoDB.',
  },
  '/sources': {
    title: 'Sources',
    subtitle: 'Evidence sources from the selected analysis.',
  },
  '/reports': {
    title: 'Reports',
    subtitle: 'Full analysis record with downloadable summary.',
  },
  '/settings': {
    title: 'Settings',
    subtitle: 'Theme, profile, analysis preferences, and system status.',
  },
};

export default function AppLayout() {
  const { pathname } = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const exact = META[pathname];
  const meta =
    exact ||
    (pathname.startsWith('/analysis/')
      ? { title: 'Analysis', subtitle: 'Saved credibility assessment.' }
      : { title: 'CrediLens', subtitle: '' });

  return (
    <div className="min-h-screen bg-cred-bg text-cred-text flex">
      <Sidebar />
      <MobileDrawer open={menuOpen} onClose={() => setMenuOpen(false)} />
      <div className="flex min-w-0 flex-1 flex-col pb-20 lg:pb-0">
        <Topbar title={meta.title} subtitle={meta.subtitle} onMenu={() => setMenuOpen(true)} />
        <main className="flex-1 px-4 py-5 lg:px-8 lg:py-6">
          <Outlet />
        </main>
        <footer className="hidden lg:block px-8 pb-6 text-xs text-muted">
          CrediLens estimates credibility; it does not certify truth.{' '}
          <Link className="text-cred-accent" to="/settings">
            Methodology
          </Link>
        </footer>
      </div>
      <MobileNavbar />
    </div>
  );
}
