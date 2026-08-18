/**
 * J.A.R.V.I.S. Navigation Module
 * Keyboard shortcuts + localStorage persistence + quick nav
 */
function navAIOS() {
  return {
    activeNav: localStorage.getItem('jarvis-active-nav') || 'command-center',
    navItems: [
      { id: 'command-center', label: 'Command Center', shortcut: '1', href: '/command-center' },
      { id: 'dashboard', label: 'Dashboard', shortcut: '2', href: '/' },
      { id: 'agents', label: 'Agents', shortcut: '3', href: '/agents' },
      { id: 'tasks', label: 'Tasks', shortcut: '4', href: '/tasks' },
      { id: 'finance', label: 'Finance', shortcut: '5', href: '/finance' },
      { id: 'kpis', label: 'KPIs', shortcut: '6', href: '/kpis' },
      { id: 'escalations', label: 'Escalations', shortcut: '7', href: '/escalations' },
      { id: 'onboarding', label: 'Onboarding', shortcut: '8', href: '/onboarding' },
    ],

    init() {
      this.bindKeyboard();
      this.syncFromURL();
    },

    bindKeyboard() {
      document.addEventListener('keydown', (e) => {
        const isInput = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA';
        if (isInput) return;

        const key = e.key;
        const mod = e.metaKey || e.ctrlKey;

        // Cmd/Ctrl + 1-8: Tab navigation
        if (mod && key >= '1' && key <= '8') {
          e.preventDefault();
          const idx = parseInt(key) - 1;
          if (this.navItems[idx]) {
            this.navigateTo(this.navItems[idx]);
          }
        }

        // Cmd/Ctrl + K: Handled by command-bar.js directly

        // Cmd/Ctrl + .: Command center
        if (mod && key === '.') {
          e.preventDefault();
          this.navigateTo(this.navItems[0]);
        }
      });
    },

    syncFromURL() {
      const path = window.location.pathname;
      const match = this.navItems.find(item => item.href === path);
      if (match) {
        this.setActive(match.id);
      }
    },

    navigateTo(item) {
      this.setActive(item.id);
      window.location.href = item.href;
    },

    setActive(id) {
      this.activeNav = id;
      localStorage.setItem('jarvis-active-nav', id);
    },

    isActive(id) {
      return this.activeNav === id;
    },

    getShortcutLabel(item) {
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const mod = isMac ? '⌘' : 'Ctrl+';
      return mod + item.shortcut;
    },
  };
}

// Auto-init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  const navEl = document.querySelector('[x-data="navAIOS()"]');
  if (navEl) {
    Alpine.data('navAIOS', navAIOS);
  }
});
