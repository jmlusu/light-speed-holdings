/* ═══════════════════════════════════════════════════════════════
   J.A.R.V.I.S. Control Plane — Offline Sync Module
   Queues failed write operations in IndexedDB and replays them
   via the Background Sync API (or periodic retry).
   Issue #41 — Wire offline-first PWA into served dashboard.
   Issue #135 — Optimistic UI + queue integration.

   CSP-safe: external file, no inline scripts.
   ═══════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const DB_NAME    = 'jarvis-offline-queue';
  const DB_VERSION = 1;
  const STORE_NAME = 'actions';
  const SYNC_TAG   = 'jarvis-offline-queue';
  const CONFLICT_STORE = 'conflicts';
  const MAX_AGE_MS = 30 * 24 * 60 * 60 * 1000; // 30 days

  /** HTTP methods that mutate state and should be queued on failure. */
  const MUTATING_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

  /** In-memory set of URLs currently queued (for optimistic UI). */
  const pendingUrls = new Set();

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

    // Track pending URL for optimistic UI.
    pendingUrls.add(url);

    // Notify listeners that an action was queued.
    window.dispatchEvent(
      new CustomEvent('offline-action-queued', {
        detail: { action, url, method: action.method },
      })
    );

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
        pendingUrls.delete(action.url);
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
    pendingUrls.clear();
  }

  /**
   * Remove a single queued action by id.
   */
  async function removeAction(id) {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const action = await idbRequest(store.get(id));
    store.delete(id);
    await idbRequest(tx.done);
    if (action) {
      // Only clear pending if no other queued action references same URL.
      const remaining = await getQueuedActions();
      if (!remaining.some((a) => a.url === action.url)) {
        pendingUrls.delete(action.url);
      }
    }
    window.dispatchEvent(new CustomEvent('offline-action-removed', { detail: { id } }));
  }

  /**
   * Re-queue a failed action (delete + re-add with fresh timestamp).
   */
  async function retryAction(id) {
    const db = await openDB();
    const tx = db.transaction(STORE_NAME, 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const action = await idbRequest(store.get(id));
    if (!action) return null;
    store.delete(id);
    await idbRequest(tx.done);

    // Re-add with fresh timestamp.
    action.timestamp = Date.now();
    const db2 = await openDB();
    const tx2 = db2.transaction(STORE_NAME, 'readwrite');
    const store2 = tx2.objectStore(STORE_NAME);
    await idbRequest(store2.add(action));
    await idbRequest(tx2.done);
    pendingUrls.add(action.url);
    requestBackgroundSync();
    window.dispatchEvent(new CustomEvent('offline-action-retried', { detail: { action } }));
    return action;
  }

  /**
   * Check if a URL is currently in the offline queue.
   */
  function isPending(url) {
    return pendingUrls.has(url);
  }

  /**
   * Get the count of queued actions.
   */
  async function getQueueCount() {
    const actions = await getQueuedActions();
    return actions.length;
  }

  /**
   * Load pending URLs from IndexedDB into the in-memory set (call on page load).
   */
  async function loadPendingFromDB() {
    const actions = await getQueuedActions();
    for (const action of actions) {
      pendingUrls.add(action.url);
    }
    return actions.length;
  }

  /**
   * Get queue statistics (count, oldest, newest).
   */
  async function getQueueStats() {
    const actions = await getQueuedActions();
    if (actions.length === 0) {
      return { count: 0, oldest: null, newest: null };
    }
    const timestamps = actions.map((a) => a.timestamp);
    return {
      count: actions.length,
      oldest: Math.min(...timestamps),
      newest: Math.max(...timestamps),
    };
  }

  /* ── Conflict store helpers (used by #136) ──────────────── */

  /**
   * Open the conflicts object store (created on demand).
   */
  async function openConflictDB() {
    const db = await openDB();
    if (!db.objectStoreNames.contains(CONFLICT_STORE)) {
      db.close();
      const db2 = await new Promise((resolve, reject) => {
        const req = indexedDB.open(DB_NAME, DB_VERSION + 1);
        req.onupgradeneeded = () => {
          const d = req.result;
          if (!d.objectStoreNames.contains(CONFLICT_STORE)) {
            d.createObjectStore(CONFLICT_STORE, {
              keyPath: 'id',
              autoIncrement: true,
            });
          }
        };
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
      });
      return db2;
    }
    return db;
  }

  /**
   * Store a conflict for later resolution.
   */
  async function storeConflict(conflict) {
    const db = await openConflictDB();
    const tx = db.transaction(CONFLICT_STORE, 'readwrite');
    const store = tx.objectStore(CONFLICT_STORE);
    await idbRequest(store.add({ ...conflict, timestamp: Date.now() }));
    await idbRequest(tx.done);
    window.dispatchEvent(new CustomEvent('offline-conflict-detected', { detail: conflict }));
  }

  /**
   * Get all unresolved conflicts.
   */
  async function getConflicts() {
    const db = await openConflictDB();
    const tx = db.transaction(CONFLICT_STORE, 'readonly');
    const store = tx.objectStore(CONFLICT_STORE);
    const all = await idbRequest(store.getAll());
    await idbRequest(tx.done);
    return all;
  }

  /**
   * Resolve a conflict by deleting it from the store.
   */
  async function resolveConflict(id) {
    const db = await openConflictDB();
    const tx = db.transaction(CONFLICT_STORE, 'readwrite');
    tx.objectStore(CONFLICT_STORE).delete(id);
    await idbRequest(tx.done);
    window.dispatchEvent(new CustomEvent('offline-conflict-resolved', { detail: { id } }));
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
    const succeeded = results.filter((r) => r.status === 'replayed');
    const failed = results.filter((r) => r.status === 'failed');
    const pending = results.filter((r) => r.status === 'pending');

    // Clear pending URLs for successfully synced actions.
    for (const r of succeeded) {
      if (r.url) pendingUrls.delete(r.url);
    }

    if (succeeded.length > 0 || failed.length > 0) {
      window.dispatchEvent(
        new CustomEvent('offline-sync-toast', {
          detail: {
            type: failed.length > 0 ? 'warning' : 'success',
            title: 'Offline Sync',
            message: `${succeeded.length} synced${failed.length ? `, ${failed.length} failed` : ''}${pending.length ? `, ${pending.length} pending` : ''}`,
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
    removeAction,
    retryAction,
    isPending,
    getQueueCount,
    getQueueStats,
    loadPendingFromDB,
    storeConflict,
    getConflicts,
    resolveConflict,
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

  /* ── Purge stale + restore pending URLs on load ─────────── */
  loadPendingFromDB().then(() => {
    purgeStale().catch(() => {});
  }).catch(() => {});
})();
