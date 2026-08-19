/* ═══════════════════════════════════════════════════════════════
   J.A.R.V.I.S. Control Plane — Offline Sync Module
   Queues failed write operations in IndexedDB and replays them
   via the Background Sync API (or periodic retry).
   Issue #41 — Wire offline-first PWA into served dashboard.

   CSP-safe: external file, no inline scripts.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const DB_NAME    = 'jarvis-offline-queue';
  const DB_VERSION = 1;
  const STORE_NAME = 'actions';
  const SYNC_TAG   = 'jarvis-offline-queue';
  const MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours

  /** HTTP methods that mutate state and should be queued on failure. */
  const MUTATING_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

  /* ── IndexedDB helpers ──────────────────────────────────── */

  function openDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME, {
            keyPath: 'id',
            autoIncrement: true,
          });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  function idbRequest(request) {
    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  /* ── Queue operations ───────────────────────────────────── */

  /**
   * Queue a failed mutating request for later replay.
   * Strips the session token (it will be re-minted on replay)
   * and stores enough metadata to reconstruct the fetch.
   */
  async function queueAction(url, options) {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);

    // Clone headers, removing auth (token is ephemeral).
    const cleanHeaders = {};
    if (options.headers) {
      const entries =
        options.headers instanceof Headers
          ? options.headers.entries()
          : Object.entries(options.headers);
      for (const [k, v] of entries) {
        if (k.toLowerCase() !== 'x-api-key') {
          cleanHeaders[k] = v;
        }
      }
    }

    const action = {
      url: url,
      method: options.method || 'POST',
      headers: cleanHeaders,
      body: options.body || null,
      timestamp: Date.now(),
      description: describeAction(url, options.method),
    };

    await idbRequest(store.add(action));
    await idbRequest(tx.done);

    // Attempt to register a background sync event.
    requestBackgroundSync();

    return action;
  }

  /**
   * Read all queued actions.
   */
  async function getQueuedActions() {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readonly');
    const store = tx.objectStore(STORE_NAME);
    const all = await idbRequest(store.getAll());
    await idbRequest(tx.done);
    return all;
  }

  /**
   * Purge expired entries (older than MAX_AGE_MS).
   */
  async function purgeStale() {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const all = await idbRequest(store.getAll());
    const cutoff = Date.now() - MAX_AGE_MS;
    for (const action of all) {
      if (action.timestamp < cutoff) {
        store.delete(action.id);
      }
    }
    await idbRequest(tx.done);
  }

  /**
   * Clear the entire queue.
   */
  async function clearQueue() {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.objectStore(STORE_NAME).clear();
    await idbRequest(tx.done);
  }

  /* ── Background sync trigger ────────────────────────────── */

  function requestBackgroundSync() {
    if (!navigator.serviceWorker || !navigator.serviceWorker.ready) return;
    navigator.serviceWorker.ready.then((reg) => {
      if (reg.sync) {
        reg.sync.register(SYNC_TAG).catch(() => {
          // Background sync not supported or quota exceeded — the SW
          // will retry on the next page load via periodic check.
        });
      }
    });
  }

  /* ── Description helper for UI display ──────────────────── */

  function describeAction(url, method) {
    const m = (method || 'POST').toUpperCase();
    if (url.includes('/approve'))   return `${m} Approve`;
    if (url.includes('/reject'))    return `${m} Reject`;
    if (url.includes('/resolve'))   return `${m} Resolve`;
    if (url.includes('/decompose')) return `${m} Decompose`;
    if (url.includes('/tasks'))     return `${m} Task`;
    return `${m} ${url.split('/').pop() || url}`;
  }

  /* ── Sync result handler ────────────────────────────────── */

  window.addEventListener('sw-sync-complete', (event) => {
    const results = event.detail || [];
    const succeeded = results.filter((r) => r.status === 'replayed').length;
    const failed = results.filter((r) => r.status === 'failed').length;
    const pending = results.filter((r) => r.status === 'pending').length;

    if (succeeded > 0 || failed > 0) {
      // Dispatch to Alpine.js toast system.
      window.dispatchEvent(
        new CustomEvent('offline-sync-toast', {
          detail: {
            type: failed > 0 ? 'warning' : 'success',
            title: 'Offline Sync',
            message: `${succeeded} synced${failed ? `, ${failed} failed` : ''}${pending ? `, ${pending} pending` : ''}`,
          },
        })
      );
    }
  });

  /* ── Public API on window.jarvisOfflineSync ──────────────── */

  window.jarvisOfflineSync = {
    queueAction,
    getQueuedActions,
    purgeStale,
    clearQueue,
    requestBackgroundSync,
    get isOnline() {
      return navigator.onLine;
    },
  };

  /* ── Connectivity listener: retry on reconnect ──────────── */

  window.addEventListener('online', () => {
    console.log('[OfflineSync] Back online — attempting sync.');
    requestBackgroundSync();
  });

  window.addEventListener('offline', () => {
    console.log('[OfflineSync] Gone offline — writes will be queued.');
  });

  /* ── Purge stale entries on load ────────────────────────── */
  purgeStale().catch(() => {});
})();
