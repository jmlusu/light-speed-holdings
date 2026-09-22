import React, { useState, useEffect } from 'react';
import { Outlet, useLocation, NavLink, useNavigate } from 'react-router-dom';
import {
  Briefcase,
  FileText,
  BarChart2,
  Settings,
  User,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
  Bell,
  Search,
  Filter,
  Download,
  Upload,
  Plus,
} from 'lucide-react';
import { cn } from '@/lib/athena/utils';

interface AthenaLayoutProps {
  userProfile?: {
    name: string;
    email: string;
    avatar?: string;
  } | null;
}

const NAV_ITEMS = [
  { path: '/athena', label: 'Dashboard', icon: BarChart2 },
  { path: '/athena/jobs', label: 'Jobs', icon: Briefcase },
  { path: '/athena/applications', label: 'Applications', icon: FileText },
  { path: '/athena/analytics', label: 'Analytics', icon: BarChart2 },
  { path: '/athena/settings', label: 'Settings', icon: Settings },
];

const RIGHT_SIDEBAR_TABS = [
  { id: 'metrics', label: 'Metrics', icon: BarChart2 },
  { id: 'filters', label: 'Filters', icon: Filter },
  { id: 'actions', label: 'Actions', icon: Plus },
];

export const AthenaLayout: React.FC<AthenaLayoutProps> = ({ userProfile }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [rightSidebarTab, setRightSidebarTab] = useState<'metrics' | 'filters' | 'actions'>('metrics');
  const [mobileLeftOpen, setMobileLeftOpen] = useState(false);
  const [mobileRightOpen, setMobileRightOpen] = useState(false);

  // Close mobile sidebars on route change
  useEffect(() => {
    setMobileLeftOpen(false);
    setMobileRightOpen(false);
  }, [location.pathname]);

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(path + '/');

  return (
    <div className="min-h-screen bg-ls-grey-light flex">
      {/* Skip link for accessibility */}
      <a href="#main-content" className="skip-link sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 px-4 py-2 bg-ls-red text-ls-white rounded-lg">
        Skip to main content
      </a>

      {/* Left Sidebar - Main Navigation */}
      <aside
        className={cn(
          'fixed left-0 top-0 z-40 h-screen bg-ls-white border-r border-ls-grey-dark/30 flex flex-col transition-all duration-300 ease-in-out',
          'lg:translate-x-0',
          leftSidebarOpen ? 'w-64' : 'w-20',
          !leftSidebarOpen && 'lg:w-20',
          mobileLeftOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
        aria-label="Main navigation"
      >
        {/* Sidebar Header */}
        <div className={cn('flex items-center justify-between p-4 border-b border-ls-grey-dark/30', !leftSidebarOpen && 'justify-center')}>
          {leftSidebarOpen && (
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-9 h-9 rounded-lg bg-ls-red flex items-center justify-center flex-shrink-0">
                <Briefcase className="w-5 h-5 text-ls-white" aria-hidden="true" />
              </div>
              <div className="min-w-0">
                <h1 className="font-display font-bold text-lg text-ls-navy truncate">Athena</h1>
                <p className="font-body text-[10px] text-ls-grey-light-text tracking-wider uppercase">Job Platform</p>
              </div>
            </div>
          )}
          {!leftSidebarOpen && (
            <div className="w-9 h-9 rounded-lg bg-ls-red flex items-center justify-center">
              <Briefcase className="w-5 h-5 text-ls-white" aria-hidden="true" />
            </div>
          )}

          <button
            onClick={() => setLeftSidebarOpen(!leftSidebarOpen)}
            className={cn(
              'p-2 rounded-lg transition-colors lg:hidden',
              'text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10'
            )}
            aria-label={leftSidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
            aria-expanded={leftSidebarOpen}
          >
            {leftSidebarOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-1" role="navigation" aria-label="Athena sections">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150',
                'text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10',
                isActive
                  ? 'bg-ls-red/10 text-ls-red border-l border-ls-red'
                  : '',
                !leftSidebarOpen && 'justify-center px-2'
              )}
              aria-current={isActive(item.path) ? 'page' : undefined}
              title={!leftSidebarOpen ? item.label : undefined}
            >
              <item.icon className={cn('w-5 h-5 flex-shrink-0', isActive(item.path) && 'text-ls-red')} aria-hidden="true" />
              {leftSidebarOpen && <span className="font-body font-medium text-sm truncate">{item.label}</span>}
            </NavLink>
          ))}

          {/* User profile at bottom */}
          {leftSidebarOpen && userProfile && (
            <div className="pt-4 border-t border-ls-grey-dark/30 mt-auto">
              <div className="flex items-center gap-3 px-3 py-2">
                <div className="w-8 h-8 rounded-full bg-ls-red flex items-center justify-center text-ls-white font-display font-bold text-sm">
                  {userProfile.name.charAt(0).toUpperCase()}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-body font-medium text-sm text-ls-navy truncate">{userProfile.name}</p>
                  <p className="font-body text-[10px] text-ls-grey-light-text truncate">{userProfile.email}</p>
                </div>
              </div>
            </div>
          )}
        </nav>

        {/* Toggle button for desktop */}
        <button
          onClick={() => setLeftSidebarOpen(!leftSidebarOpen)}
          className={cn(
            'absolute -right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-full',
            'bg-ls-white border border-ls-grey-dark/30 shadow-lg',
            'text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/5',
            'lg:block hidden',
            !leftSidebarOpen && 'rotate-180'
          )}
          aria-label={leftSidebarOpen ? 'Collapse navigation' : 'Expand navigation'}
          aria-expanded={leftSidebarOpen}
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
      </aside>

      {/* Mobile left sidebar overlay */}
      {mobileLeftOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setMobileLeftOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Main Content Area */}
      <main
        id="main-content"
        className={cn(
          'flex-1 flex flex-col min-w-0 transition-all duration-300',
          leftSidebarOpen ? 'lg:ml-64' : 'lg:ml-20',
          rightSidebarOpen ? 'lg:mr-80' : 'lg:mr-0'
        )}
        tabIndex={-1}
      >
        {/* Top Bar */}
        <header className="sticky top-0 z-20 bg-ls-white/95 backdrop-blur-sm border-b border-ls-grey-dark/30">
          <div className="flex items-center justify-between px-4 sm:px-6 py-3 sm:py-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setMobileLeftOpen(true)}
                className="lg:hidden p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10"
                aria-label="Open navigation menu"
              >
                <Menu className="w-6 h-6" />
              </button>

              {/* Page title from route */}
              <div className="hidden sm:block">
                <h1 className="font-display font-bold text-xl text-ls-navy">
                  {NAV_ITEMS.find(item => isActive(item.path))?.label || 'Athena'}
                </h1>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Search */}
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ls-grey-light-text" aria-hidden="true" />
                <input
                  type="search"
                  placeholder="Search jobs, companies..."
                  className="w-64 pl-10 pr-4 py-2 bg-ls-grey-light border border-ls-grey-dark/30 rounded-lg text-sm text-ls-navy placeholder-ls-grey-light-text focus:outline-none focus:ring-2 focus:ring-ls-red focus:border-transparent"
                  aria-label="Search"
                />
              </div>

              {/* Notifications */}
              <button
                className="relative p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors"
                aria-label="Notifications"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-ls-red rounded-full" aria-hidden="true" />
              </button>

              {/* Right sidebar toggle */}
              <button
                onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
                className={cn(
                  'p-2 rounded-lg transition-colors',
                  'text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10',
                  rightSidebarOpen && 'lg:bg-ls-red/10 lg:text-ls-red'
                )}
                aria-label={rightSidebarOpen ? 'Close right panel' : 'Open right panel'}
                aria-expanded={rightSidebarOpen}
              >
                <Filter className="w-5 h-5" />
              </button>

              {/* Mobile right sidebar toggle */}
              <button
                onClick={() => setMobileRightOpen(true)}
                className="lg:hidden p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10"
                aria-label="Open filters panel"
              >
                <Filter className="w-5 h-5" />
              </button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-4 sm:p-6">
          <Outlet />
        </div>
      </main>

      {/* Right Sidebar - Metrics/Filters/Actions */}
      <aside
        className={cn(
          'fixed right-0 top-0 z-40 h-screen bg-ls-white border-l border-ls-grey-dark/30 flex flex-col transition-all duration-300 ease-in-out',
          'lg:translate-x-0',
          rightSidebarOpen ? 'w-80' : 'w-0 lg:w-0',
          !rightSidebarOpen && 'lg:w-0 overflow-hidden',
          mobileRightOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'
        )}
        aria-label="Metrics and filters"
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between p-4 border-b border-ls-grey-dark/30">
          <h2 className="font-display font-bold text-lg text-ls-navy">Panel</h2>
          <button
            onClick={() => setRightSidebarOpen(false)}
            className="p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors lg:hidden"
            aria-label="Close panel"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-ls-grey-dark/30 px-2" role="tablist" aria-label="Right panel tabs">
          {RIGHT_SIDEBAR_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setRightSidebarTab(tab.id as 'metrics' | 'filters' | 'actions')}
              className={cn(
                'flex-1 flex items-center justify-center gap-2 px-3 py-2.5 rounded-t-lg transition-all duration-150',
                'text-ls-grey-dark hover:text-ls-red',
                rightSidebarTab === tab.id
                  ? 'bg-ls-red/10 text-ls-red border-b-2 border-ls-red font-medium'
                  : 'font-normal',
                rightSidebarOpen || 'lg:flex-1'
              )}
              role="tab"
              aria-selected={rightSidebarTab === tab.id}
              aria-controls={`panel-${tab.id}`}
              id={`tab-${tab.id}`}
            >
              <tab.icon className="w-4 h-4" aria-hidden="true" />
              <span className="hidden sm:inline font-body text-sm">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tab Panels */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Metrics Panel */}
          <div
            id="panel-metrics"
            role="tabpanel"
            aria-labelledby="tab-metrics"
            hidden={rightSidebarTab !== 'metrics'}
            className="space-y-4 animate-in fade-in"
          >
            <div className="flex items-center justify-between">
              <h3 className="font-display font-bold text-base text-ls-navy">Quick Stats</h3>
              <button className="p-1 rounded text-ls-grey-dark hover:text-ls-red" aria-label="Refresh metrics">
                <Download className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-3" id="metrics-content">
              {/* Metrics will be injected by pages */}
            </div>
          </div>

          {/* Filters Panel */}
          <div
            id="panel-filters"
            role="tabpanel"
            aria-labelledby="tab-filters"
            hidden={rightSidebarTab !== 'filters'}
            className="space-y-4 animate-in fade-in"
          >
            <h3 className="font-display font-bold text-base text-ls-navy">Filters</h3>
            <div id="filters-content" className="space-y-4">
              {/* Filters will be injected by pages */}
            </div>
          </div>

          {/* Actions Panel */}
          <div
            id="panel-actions"
            role="tabpanel"
            aria-labelledby="tab-actions"
            hidden={rightSidebarTab !== 'actions'}
            className="space-y-4 animate-in fade-in"
          >
            <h3 className="font-display font-bold text-base text-ls-navy">Quick Actions</h3>
            <div className="space-y-2" id="actions-content">
              <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white hover:border-ls-red/30 hover:bg-ls-red/5 transition-all text-left">
                <Upload className="w-5 h-5 text-ls-red" aria-hidden="true" />
                <span className="font-body font-medium text-sm text-ls-navy">Upload Resume</span>
              </button>
              <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white hover:border-ls-red/30 hover:bg-ls-red/5 transition-all text-left">
                <Plus className="w-5 h-5 text-ls-cyan" aria-hidden="true" />
                <span className="font-body font-medium text-sm text-ls-navy">Add Job Manually</span>
              </button>
              <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-ls-grey-dark/30 bg-ls-white hover:border-ls-red/30 hover:bg-ls-red/5 transition-all text-left">
                <Download className="w-5 h-5 text-emerald-600" aria-hidden="true" />
                <span className="font-body font-medium text-sm text-ls-navy">Export Data</span>
              </button>
              <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors">
                <Plus className="w-5 h-5" aria-hidden="true" />
                <span>New Application</span>
              </button>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile right sidebar overlay */}
      {mobileRightOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setMobileRightOpen(false)}
          aria-hidden="true"
        />
      )}
    </div>
  );
};

export default AthenaLayout;
