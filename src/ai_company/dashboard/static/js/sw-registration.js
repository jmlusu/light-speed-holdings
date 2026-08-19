/* ═══════════════════════════════════════════════════════════════
   J.A.R.V.I.S. Control Plane — Service Worker Registration
   Handles SW lifecycle, update prompts, and A2HS deferred prompt.
   Issue #41 — Wire offline-first PWA into served dashboard.

   CSP-safe: external file, no inline scripts.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  if (!('serviceWorker' in navigator)) {
    console.warn('[SW-Reg] Service workers not supported — offline features disabled.');
    return;
  }

  /* ── Deferred install prompt (A2HS) ─────────────────────── */
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    // Expose to Alpine.js via a CustomEvent so the dashboard can
    // show an "Install" button without modifying every page.
    window.dispatchEvent(new CustomEvent('sw-installable', { detail: true }));
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    window.dispatchEvent(new CustomEvent('sw-installable', { detail: false }));
  });

  /**
   * Trigger the deferred A2HS prompt.
   * Returns a promise resolving to 'accepted' or 'dismissed'.
   * Safe to call even if no prompt is available (returns null).
   */
  window.jarvisInstall = async function () {
    if (!deferredPrompt) return null;
    deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    deferredPrompt = null;
    return result.outcome;
  };

  /* ── Service worker registration ────────────────────────── */

  let refreshing = false;

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (refreshing) return;
    refreshing = true;
    // A new SW has taken control — reload once to pick up fresh assets.
    window.location.reload();
  });

  navigator.serviceWorker.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SYNC_COMPLETE') {
      // Dispatch to Alpine.js stores for UI feedback.
      window.dispatchEvent(
        new CustomEvent('sw-sync-complete', { detail: event.data.results })
      );
    }
  });

  async function register() {
    try {
      const reg = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
      });

      // Check for updates periodically (every 60 minutes).
      setInterval(() => reg.update(), 60 * 60 * 1000);

      // Listen for a new waiting SW and notify the UI.
      if (reg.waiting) {
        window.dispatchEvent(new CustomEvent('sw-update-available'));
      }
      reg.addEventListener('updatefound', () => {
        const newWorker = reg.installing;
        if (!newWorker) return;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            window.dispatchEvent(new CustomEvent('sw-update-available'));
          }
        });
      });

      console.log('[SW-Reg] Registered, scope:', reg.scope);
    } catch (err) {
      console.warn('[SW-Reg] Registration failed:', err);
    }
  }

  register();
})();
